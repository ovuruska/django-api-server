from django.db import models


class Payroll(models.Model):
	employee_name = models.CharField(max_length=128)
	start = models.DateTimeField()
	end = models.DateTimeField()
	tips = models.DecimalField(max_digits=10, decimal_places=2)
	service_cost = models.DecimalField(max_digits=10, decimal_places=2)
	product_cost = models.DecimalField(max_digits=10, decimal_places=2)
	working_hours = models.IntegerField()