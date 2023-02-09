

def extract_role(func):
	def wrapper(self, request, view):
		if getattr(request.user,"employee",None) is not None:
			request.user.role = request.user.employee.role
		elif getattr(request.user,"customer",None) is not None:
			request.user.role = request.user.customer.role

		return func(self, request, view)
	return wrapper
