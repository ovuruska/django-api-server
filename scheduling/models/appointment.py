from django.db import models
from django.utils.translation import gettext_lazy as _

from scheduling.common import BaseModel


class Appointment(BaseModel):
	class Status(models.TextChoices):
		PENDING = 'Pending', _('Pending')
		CONFIRMED = 'Confirmed', _('Confirmed')
		COMPLETED = 'Completed', _('Completed')
		CANCELLED = 'Cancelled', _('Cancelled')

	class AppointmentType(models.TextChoices):
		FULL_GROOMING = 'Full Grooming', _('Full Grooming')
		WE_WASH = 'We Wash', _('We Wash')

	customer = models.ForeignKey("Customer", on_delete=models.DO_NOTHING, related_name="appointments", blank=False)
	dog = models.ForeignKey("Dog", on_delete=models.CASCADE, related_name="appointments", blank=False)
	start = models.DateTimeField()
	end = models.DateTimeField()
	customer_notes = models.TextField()
	employee_notes = models.TextField()
	services = models.ManyToManyField("Service", related_name="appointments", blank=True,default=[])
	tip = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	cost = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	products = models.ManyToManyField("Product", related_name="products+", blank=True)
	branch = models.ForeignKey("Branch", on_delete=models.DO_NOTHING, related_name="appointments", blank=False)
	employee = models.ForeignKey("Employee", on_delete=models.DO_NOTHING, related_name="appointments", blank=True,
	                             null=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

	appointment_type = models.CharField(max_length=20, choices=AppointmentType.choices, default=AppointmentType.WE_WASH)

	def is_modifiable(self):
		return self.status != self.Status.COMPLETED

