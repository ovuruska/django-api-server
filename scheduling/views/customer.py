import json

from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from firebase_admin import auth
from ..models.Customer import Customer
from ..serializers.Customer import CustomerSerializer

class CustomerRetrieveAPIView(RetrieveAPIView):
	serializer_class = CustomerSerializer
	queryset = Customer.objects.all()

	def get(self, request, *args, **kwargs):
		authorization = request.META.get("HTTP_AUTHORIZATION",None)
		if authorization is None:
			return Response({"error": "No authorization header"}, status=401,
			                headers={"Content-Type": "application/json"})
		authorization = authorization.split(" ")
		if len(authorization) != 2:
			return Response({"error": "Invalid authorization header"}, status=401,headers={"Content-Type": "application/json"})

		else:
			result = auth.verify_id_token(authorization[1])
			if result is None:
				return Response({"error": "Not authorized"}, status=401,headers={"Content-Type": "application/json"})
			uid = self.kwargs["uid"]
			customer,_ = Customer.objects.get_or_create(uid=uid)

			customer_repr = CustomerSerializer().to_representation(customer)
			return Response(json.dumps(customer_repr), status=200,headers={"Content-Type": "application/json"})

