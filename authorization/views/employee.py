from knox.models import AuthToken
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from scheduling.serializers.auth import UserSerializer


class EmployeeLoginView(GenericAPIView):

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data
		employee = user.employee
		return Response({
			"user": UserSerializer(user, context=self.get_serializer_context()).data,
			"token": AuthToken.objects.create(user)[1],
			"profile":employee
		})