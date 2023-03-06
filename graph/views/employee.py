from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.http import HttpResponse, HttpResponseForbidden
from graphene_django.views import GraphQLView
from knox.models import AuthToken
from knox.settings import knox_settings, CONSTANTS
from knox.views import LoginView
from rest_framework.response import Response
from rest_framework.serializers import DateTimeField
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED

from common.extract_role import extract_role, get_role, is_employee
from graph.schema import EmployeeSchema


class EmployeeLoginMixin(LoginView):
	"""
	Ensure that the user has the employee role.

	"""
	# Dispatch post request to GraphQLView


class EmployeeGraphQL(GraphQLView ):

	schema = EmployeeSchema
	graphiql = True

	@staticmethod
	def get_user_from_token(token):
		objs = AuthToken.objects.filter(token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH])
		if len(objs) == 0:
			return None
		return objs.first().user

	def dispatch(self, request, *args, **kwargs):
		# Check if user has employee role
		# Implement  authorization header

		token = request.META.get('HTTP_AUTHORIZATION',None)

		if token is None:
			return HttpResponseForbidden("You are not signed in.")

		user = self.get_user_from_token(token.split(" ")[1])
		request.user = user
		request.user = user
		if is_employee(request):
			return super().dispatch(request, *args, **kwargs)

		return HttpResponseForbidden("You are not authorized to access this resource")
