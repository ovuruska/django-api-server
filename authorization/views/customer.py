from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.forms import model_to_dict
from knox.models import AuthToken

from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny

from authorization.serializers.requests.login_customer import LoginCustomerRequestSerializer
from authorization.serializers.requests.register_customer import RegisterCustomerRequestSerializer
from common.validate_request import validate_request
from scheduling.models import Customer
from scheduling.serializers.auth import UserSerializer, LoginUserSerializer, CreateUserSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class CustomerVerifyTokenView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		return Response(status=status.HTTP_200_OK)


class CustomerRegisterAPIView(CreateAPIView, PermissionRequiredMixin):
	permission_classes = [AllowAny]
	serializer_class = RegisterCustomerRequestSerializer

	@validate_request(RegisterCustomerRequestSerializer)
	def create(self, request, *args, **kwargs):
		serialized_data = kwargs.get("serialized_data")
		email = serialized_data.get("email")
		password = serialized_data.get("password")
		try:
			user = User.objects.create_user(username=email, password=password)
		except IntegrityError:
			return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

		first_name = serialized_data.get("first_name")
		last_name = serialized_data.get("last_name")
		name = f"{first_name} {last_name}"
		customer = Customer.objects.create(user=user,name=name)
		return Response({"user": UserSerializer(user, context=self.get_serializer_context()).data,
		                 "token": AuthToken.objects.create(user)[1], "profile": model_to_dict(customer)})


class CustomerLoginAPIView(GenericAPIView, PermissionRequiredMixin):
	permission_classes = [AllowAny]
	serializer_class = LoginCustomerRequestSerializer

	@validate_request(LoginCustomerRequestSerializer)
	def post(self, request, *args, **kwargs):
		serialized_data = kwargs.get("serialized_data")
		email = serialized_data.get("email")
		password = serialized_data.get("password")
		user = User.objects.get(username=email)
		if not user.check_password(password):
			return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
		else:
			customer = Customer.objects.get(user=user)
			return Response({"user": UserSerializer(user, context=self.get_serializer_context()).data,
			                 "token": AuthToken.objects.create(user)[1], "profile": model_to_dict(customer)})
