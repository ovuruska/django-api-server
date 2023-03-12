from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common import BaseModel


class Appointment(BaseModel):
	class Status(models.TextChoices):
		PENDING = 'Pending', _('Pending')
		CONFIRMED = 'Confirmed', _('Confirmed')
		COMPLETED = 'Completed', _('Completed')
		CANCELLED = 'Cancelled', _('Cancelled')
		RESCHEDULING = "Rescheduling", _("Rescheduling")
		CHECKED_IN = "CheckedIn", _("Checked In")
		PICKUP_READY = "PickUpReady", _("Pickup Ready")
		NO_SHOW = "NoShow", _("No Show")
		CLOSED_CHARGED = "ClosedCharged", _("Closed Charged")

	class AppointmentType(models.TextChoices):
		FULL_GROOMING = 'Full Grooming', _('Full Grooming')
		WE_WASH = 'We Wash', _('We Wash')

	customer = models.ForeignKey("Customer", on_delete=models.DO_NOTHING, related_name="appointments", blank=False)
	dog = models.ForeignKey("Dog", on_delete=models.DO_NOTHING, related_name="appointments", blank=False)
	start = models.DateTimeField(default=timezone.now)
	end = models.DateTimeField(default=timezone.now)
	customer_notes = models.TextField(blank=True, max_length=1000)
	employee_notes = models.TextField(blank=True, max_length=1000)
	services = models.ManyToManyField("Service", related_name="appointments", blank=True, default=[])
	tip = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	cost = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	products = models.ManyToManyField("Product", related_name="products+", blank=True, default=[])
	branch = models.ForeignKey("Branch", on_delete=models.CASCADE, related_name="appointments", blank=False)
	employee = models.ForeignKey("Employee", on_delete=models.DO_NOTHING, related_name="appointments", blank=True, null=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

	appointment_type = models.CharField(max_length=20, choices=AppointmentType.choices, default=AppointmentType.WE_WASH)
	reminder_sent = models.DateTimeField(blank=True, null=True)
	check_in = models.DateTimeField(blank=True, null=True)
	pick_up = models.DateTimeField(blank=True, null=True)
	confirmed_on = models.DateTimeField(blank=True, null=True)

	checkout_time = models.DateTimeField(blank=True, null=True)
	checkout_status = models.BooleanField(default=False)


	def is_modifiable(self):
		return self.status != self.Status.COMPLETED

	def is_available(self):
		return self.status in [self.Status.PENDING, self.Status.RESCHEDULING]

	class Meta:
		ordering = ['-start']
