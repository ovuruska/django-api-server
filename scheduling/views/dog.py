from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView,  DestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from common.pagination import pagination
from scheduling.models import Dog, Customer
from scheduling.serializers.Dog import DogSerializer, DogCreateSerializer


class PetCreateAPIView(generics.CreateAPIView):
    serializer_class = DogCreateSerializer

    def post(self, request, *args, **kwargs):
        # retrieve authenticated customer from request.user and set as owner
        customer = Customer.objects.get(user=request.user)
        request.data["owner"] = customer.id

        # check if dog with the same name already exists for the customer
        dog_name = request.data.get('name')
        if customer.dogs.filter(name=dog_name).exists():
            return Response({"error": "Dog with this name already exists for this customer."},
                            status=status.HTTP_400_BAD_REQUEST)

        # create the dog instance
        return super().create(request, *args, **kwargs)


class PetModifyRetrieveDestroyAPIView(RetrieveAPIView, DestroyAPIView, UpdateAPIView):
    serializer_class = DogSerializer
    queryset = Dog.objects.all()

    def get_queryset(self):
        if 'pk' in self.kwargs:
            return self.queryset.filter(id=self.kwargs['pk'])
        return self.queryset.none()

    def patch(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        dog = Dog.objects.get(id=pk)
        if dog.owner == Customer.objects.get(user=request.user):
            serializer = self.serializer_class(dog, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "The dog is not registered for this customer."},
                            status=status.HTTP_400_BAD_REQUEST)



class PetFilterView(generics.ListAPIView):
    serializer_class = DogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = "__all__"

    def get_queryset(self):
        queryset = Dog.objects.all()
        queryset = pagination(self.request, queryset)
        return queryset
