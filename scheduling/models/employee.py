from django.db import models
from django.utils.translation import gettext_lazy as _

from scheduling.common import BaseModel


class Employee(BaseModel):
	class Role(models.TextChoices):
		FULL_GROOMING = 'Full Grooming', _('Full Grooming')
		WE_WASH = 'We Wash', _('We Wash')

	name = models.CharField(max_length=128)
	phone = models.CharField(max_length=16)
	email = models.CharField(max_length=64)
	role = models.CharField(max_length=16, choices=Role.choices, default=Role.WE_WASH)
	branch = models.ForeignKey("scheduling.Branch", on_delete=models.CASCADE, related_name='employees')
	uid = models.CharField(max_length=64)

	def is_groomer(self):
		return self.role == self.Role.FULL_GROOMING

	def __str__(self):
		return self.name
