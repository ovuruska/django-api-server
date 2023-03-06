from common.roles import Roles

def get_role(request):
	if getattr(request.user,"employee",None) is not None:
		return request.user.employee.role
	elif getattr(request.user,"customer",None) is not None:
		return request.user.customer.role
	else:
		return  Roles.ANONYMOUS

def is_employee(request):
	return get_role(request) >= Roles.EMPLOYEE_WE_WASH


def is_customer(request):
	return get_role(request) == Roles.CUSTOMER

def extract_role(func):
	def wrapper(self, request, view):
		request.user.role = get_role(request)
		return func(self, request, view)
	return wrapper



