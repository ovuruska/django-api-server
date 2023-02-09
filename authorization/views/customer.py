from django.forms import model_to_dict
from knox.models import AuthToken
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from scheduling.serializers.auth import UserSerializer, LoginUserSerializer


class CustomerLoginAPIView(GenericAPIView):

	serializer_class = LoginUserSerializer
	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data
		customer = user.customer
		return Response({
			"user": UserSerializer(user, context=self.get_serializer_context()).data,
			"token": AuthToken.objects.create(user)[1],
			"profile":model_to_dict(customer)
		})