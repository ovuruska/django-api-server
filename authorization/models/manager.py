from scheduling.models import Employee


class Manager(Employee):

	class Meta:
		proxy = True
		verbose_name = 'Manager'
		verbose_name_plural = 'Managers'