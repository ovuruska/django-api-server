from django.db import models

class EmployeeWorkingHours(models.Model):
	employee = models.ForeignKey('scheduling.Employee', on_delete=models.CASCADE)
	date = models.DateField()
	branch = models.ForeignKey('scheduling.Branch', on_delete=models.CASCADE)
	start = models.TimeField()
	end = models.TimeField()
