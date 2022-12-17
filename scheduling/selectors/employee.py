from scheduling.models import Employee


def get_groomers(branch_name=None):
	"""
	:param branch_name: The name of the branch to get groomers from
	:return: A list of groomers

	"""
	if branch_name is None:
		return Employee.objects.filter(role=Employee.Staff.GROOMER)

	else:
		return Employee.objects.filter(role=Employee.Staff.GROOMER, branch__name=branch_name)
