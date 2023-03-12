from common.roles import Roles

def get_role_from_int(role_int) -> str:
	if role_int == 0:
		return "Anonymous"
	elif role_int == 1:
		return "Customer"
	elif role_int == 10:
		return "We Wash"
	elif role_int == 15:
		return "Full Grooming"
	elif role_int == 20:
		return "Accountant"
	elif role_int == 30:
		return "Manager"
	elif role_int == 40:
		return "Admin"
	else:
		return "Anonymous"


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



