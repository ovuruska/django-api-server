from scheduling.models import Employee


class Accountant(Employee):
	class Meta:
		proxy = True
		verbose_name = 'Accountant'
		verbose_name_plural = 'Accountants'