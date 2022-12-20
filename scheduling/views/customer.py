import json

from firebase_admin import auth
from rest_framework.generics import RetrieveAPIView,ListAPIView
from rest_framework.response import Response

from ..models import Dog
from ..models.customer import Customer
from ..serializers.Customer import CustomerSerializer
from ..serializers.Dog import DogSerializer


class CustomerDogsRetrieveAPIView(ListAPIView):
	serializer_class = CustomerSerializer

	def get_queryset(self):
		uid = self.kwargs['uid']
		return Customer.objects.filter(uid=uid)

	def list(self, request, *args, **kwargs):
		queryset = self.get_queryset()
		dogs = Dog.objects.filter(owner=queryset[0].id)
		serializer = DogSerializer(dogs , many=True)
		return Response(serializer.data)

class CustomerRetrieveAPIView(RetrieveAPIView):
	serializer_class = CustomerSerializer
	queryset = Customer.objects.all()

	def get(self, request, *args, **kwargs):
		authorization = request.META.get("HTTP_AUTHORIZATION", None)
		if authorization is None:
			return Response({"error": "No authorization header"}, status=401,
			                headers={"Content-Type": "application/json"})
		authorization = authorization.split(" ")
		if len(authorization) != 2:
			return Response({"error": "Invalid authorization header"}, status=401,
			                headers={"Content-Type": "application/json"})

		else:
			result = auth.verify_id_token(authorization[1])
			if result is None:
				return Response({"error": "Not authorized"}, status=401, headers={"Content-Type": "application/json"})
			uid = self.kwargs["uid"]
			customer, _ = Customer.objects.get_or_create(uid=uid)

			customer_repr = CustomerSerializer().to_representation(customer)
			return Response(json.dumps(customer_repr), status=200, headers={"Content-Type": "application/json"})
