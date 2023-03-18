from django.apps import apps

from common.roles import Roles


def get_groomers(branch_name=None):
	"""
	:param branch_name: The name of the branch to get groomers from
	:return: A list of groomers

	"""
	Employee = apps.get_model('scheduling', 'Employee')

	if branch_name is None:
		return Employee.objects.filter(role=Roles.EMPLOYEE_FULL_GROOMING)

	else:
		return Employee.objects.filter(role=Roles.EMPLOYEE_FULL_GROOMING, branch__name=branch_name)
