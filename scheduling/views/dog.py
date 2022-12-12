from rest_framework.generics import RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView

from scheduling.models import Dog,Customer
from scheduling.serializers.Dog import DogSerializer



class DogCreateAPIView(CreateAPIView):
	serializer_class = DogSerializer
	queryset = Dog.objects.all()

	def post(self, request, *args, **kwargs):
		try:
			request.data._mutable = True
		except AttributeError:
			pass
		owner_id = request.data["owner"]
		customer_instance = Customer.objects.get_or_create(uid=owner_id)
		if type(customer_instance) is tuple:
			customer_instance = customer_instance[0]
		request.data["owner"] = customer_instance.id
		dog_name = request.data["name"]
		try:
			_ = Dog.objects.get(name=dog_name)
			return Response({"message": "Dog already exists"}, status=400)
		except Dog.DoesNotExist:
			return self.create(request, *args, **kwargs)


class DogModifyRetrieveDestroyAPIView(RetrieveAPIView, DestroyAPIView, UpdateAPIView):
	serializer_class = DogSerializer
	queryset = Dog.objects.all()
	
