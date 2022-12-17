from rest_framework.generics import RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from scheduling.models import Dog,Customer
from scheduling.serializers.Dog import DogSerializer
from scheduling.services.dog import is_dog_available


class DogCreateAPIView(CreateAPIView):
	serializer_class = DogSerializer
	queryset = Dog.objects.all()

	def post(self, request, *args, **kwargs):
		try:
			request.data._mutable = True
		except AttributeError:
			pass
		owner_id = request.data["owner"]
		dog_name = request.data["name"]
		if is_dog_available(owner_id,dog_name):
			return Response({"message":"Dog already exists"})
		else:
			return self.create(request, *args, **kwargs)


class DogModifyRetrieveDestroyAPIView(RetrieveAPIView, DestroyAPIView, UpdateAPIView):
	serializer_class = DogSerializer
	queryset = Dog.objects.all()
	
