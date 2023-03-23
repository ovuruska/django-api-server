
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
			return "We Wash"
		elif role == Roles.EMPLOYEE_FULL_GROOMING:
			return "Full Grooming"
		elif role == Roles.ACCOUNTANT:
			return "Accountant"
		elif role == Roles.MANAGER:
			return "Manager"
		elif role == Roles.ADMIN:
			return "Admin"
		else:
			return "Anonymous"


	@staticmethod
	def get_role_choices(role:str):
		if role == "Customer":
			return Roles.CUSTOMER
		elif role == "We Wash":
			return Roles.EMPLOYEE_WE_WASH
		elif role == "Full Grooming":
			return Roles.EMPLOYEE_FULL_GROOMING
		elif role == "Accountant":
			return Roles.ACCOUNTANT
		elif role == "Manager":
			return Roles.MANAGER
		elif role == "Admin":
			return Roles.ADMIN
		else:
			return Roles.ANONYMOUS
