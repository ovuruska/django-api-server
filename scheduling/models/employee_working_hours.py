from django.db import models

class EmployeeWorkingHours(models.Model):
	employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE)
	weekday = models.IntegerField()
	branch = models.ForeignKey('branches.Branch', on_delete=models.CASCADE)
	start = models.TimeField()
	end = models.TimeField()
