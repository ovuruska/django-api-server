from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _

from scheduling.common import BaseModel


class Appointment(BaseModel):
	class Status(models.TextChoices):
		PENDING = 'Pending', _('Pending')
		CONFIRMED = 'Confirmed', _('Confirmed')
		COMPLETED = 'Completed', _('Completed')
		CANCELLED = 'Cancelled', _('Cancelled')
		RESCHEDULING = "Rescheduling", _("Rescheduling")

	class AppointmentType(models.TextChoices):
		FULL_GROOMING = 'Full Grooming', _('Full Grooming')
		WE_WASH = 'We Wash', _('We Wash')

	customer = models.ForeignKey("Customer", on_delete=models.DO_NOTHING, related_name="appointments", blank=False)
	dog = models.ForeignKey("Dog", on_delete=models.CASCADE, related_name="appointments", blank=False)
	start = models.DateTimeField(default=timezone.now)
	end = models.DateTimeField(default=timezone.now)
	customer_notes = models.TextField(blank=True)
	employee_notes = models.TextField(blank = True)
	services = models.ManyToManyField("Service", related_name="appointments", blank=True,default=[])
	tip = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	cost = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	products = models.ManyToManyField("Product", related_name="products+", blank=True,default=[])
	branch = models.ForeignKey("Branch", on_delete=models.DO_NOTHING, related_name="appointments", blank=False)
	employee = models.ForeignKey("Employee", on_delete=models.DO_NOTHING, related_name="appointments", blank=True,
	                             null=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

	appointment_type = models.CharField(max_length=20, choices=AppointmentType.choices, default=AppointmentType.WE_WASH)

	def is_modifiable(self):
		return self.status != self.Status.COMPLETED


	def is_available(self):
		return self.status in [self.Status.PENDING, self.Status.RESCHEDULING]