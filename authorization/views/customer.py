from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import model_to_dict
from knox.models import AuthToken
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from scheduling.models import Customer
from scheduling.serializers.auth import UserSerializer, LoginUserSerializer, CreateUserSerializer


class CustomerRegisterAPIView(GenericAPIView, PermissionRequiredMixin):
	serializer_class = CreateUserSerializer
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		customer = Customer.objects.create(user=user)
		return Response({"user": UserSerializer(user, context=self.get_serializer_context()).data,
			"token": AuthToken.objects.create(user)[1], "profile": model_to_dict(customer)})


class CustomerLoginAPIView(GenericAPIView, PermissionRequiredMixin):
	serializer_class = LoginUserSerializer
	permission_classes = [AllowAny]


	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data
		customer = user.customer
		return Response({"user": UserSerializer(user, context=self.get_serializer_context()).data,
			"token": AuthToken.objects.create(user)[1], "profile": model_to_dict(customer)})
