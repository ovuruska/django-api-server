from rest_framework.generics import RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView

from scheduling.models import Dog,Customer
from scheduling.serializers.Dog import DogSerializer



class DogModifyAPIView(CreateAPIView):
	serializer_class = DogSerializer
	queryset = Dog.objects.all()

	def post(self, request, *args, **kwargs):
		request.data._mutable = True
		owner_id = request.data["owner"]
		customer_instance = Customer.objects.get(uid=owner_id)
		request.data["owner"] = customer_instance.id
		return self.create(request, *args, **kwargs)


class DogRetrieveAPIView(RetrieveAPIView,DestroyAPIView,UpdateAPIView):
	serializer_class = DogSerializer
	queryset = Dog.objects.all()
	
