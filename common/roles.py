
class Roles:

	ANONYMOUS = 0
	CUSTOMER = 1
	EMPLOYEE_WE_WASH = 10
	EMPLOYEE_FULL_GROOMING = 15
	ACCOUNTANT = 20
	MANAGER = 30
	ADMIN = 40
	CHOICES = (
		(CUSTOMER, CUSTOMER),
		(EMPLOYEE_WE_WASH, EMPLOYEE_WE_WASH),
		(EMPLOYEE_FULL_GROOMING, EMPLOYEE_FULL_GROOMING),
		(ACCOUNTANT, ACCOUNTANT),
		(MANAGER, MANAGER),
		(ADMIN, ADMIN),

	)

	@staticmethod
	def get_role_name(role):
		if role == Roles.CUSTOMER:
			return "Customer"
		elif role == Roles.EMPLOYEE_WE_WASH:
			return "Employee We Wash"
		elif role == Roles.EMPLOYEE_FULL_GROOMING:
			return "Employee Full Grooming"
		elif role == Roles.ACCOUNTANT:
			return "Accountant"
		elif role == Roles.MANAGER:
			return "Manager"
		elif role == Roles.ADMIN:
			return "Admin"
		else:
			return "Anonymous"