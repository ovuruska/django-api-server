from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from common.pagination import pagination
from scheduling.models import Dog, Customer
from scheduling.serializers.Dog import DogSerializer, DogCreateSerializer
from scheduling.services.dog import is_dog_available


class PetCreateAPIView(generics.CreateAPIView):
    serializer_class = DogCreateSerializer

    def create(self, request, *args, **kwargs):
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


class PetFilterView(generics.ListAPIView):

	serializer_class = DogSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = "__all__"

	def get_queryset(self):
		queryset = Dog.objects.all()
		queryset = pagination(self.request, queryset)
		return queryset
