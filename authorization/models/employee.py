from scheduling.models import Employee


class EmployeeAuth(Employee):

	class Meta:
		proxy = True
		verbose_name = 'Employee'
		verbose_name_plural = 'Employees'

