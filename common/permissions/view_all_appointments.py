from rest_framework.permissions import BasePermission

from common.extract_role import extract_role
from common.roles import Roles


class CanViewAllAppointments(BasePermission):

	"""
	Allow access to all appointments if user is an employee

	"""
	@extract_role
	def has_permission(self, request, view):
		"""
		Allow access to all appointments if user is an employee
		"""
		return request.user.role > Roles.CUSTOMER
