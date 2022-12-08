from django.db import models

from scheduling.common import BaseModel


class Appointment(BaseModel):
	customer = models.ForeignKey("Customer", on_delete=models.DO_NOTHING, related_name="appointments",blank=False)
	dog = models.ForeignKey("Dog", on_delete=models.CASCADE, related_name="appointments",blank=False)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	customer_notes = models.TextField()
	employee_notes = models.TextField()
	services = models.ManyToManyField("Service", related_name="appointments",blank=False)
	tip = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	cost = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	products = models.ManyToManyField("Product", related_name="products+",blank=True)
	branch = models.ForeignKey("Branch", on_delete=models.DO_NOTHING, related_name="appointments",blank=False)
	employee = models.ForeignKey("Employee", on_delete=models.DO_NOTHING, related_name="appointments",blank=True, null=True)
