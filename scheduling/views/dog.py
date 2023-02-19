from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from common.pagination import pagination
from scheduling.models import Dog, Customer
from scheduling.serializers.Dog import DogSerializer
from scheduling.services.dog import is_dog_available


class PetCreateAPIView(CreateAPIView):
	serializer_class = DogSerializer
	queryset = Dog.objects.all()

	def post(self, request, *args, **kwargs):
		try:
			request.data._mutable = True
		except AttributeError:
			pass
		request.data['owner'] = Customer.objects.get(uid=request.data['owner']).id
		if is_dog_available(request.data["owner"], request.data["name"]):
			return Response({"message": "Dog already exists"})
		else:
			return self.create(request, *args, **kwargs)


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
