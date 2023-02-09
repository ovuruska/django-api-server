from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from common import BaseModel


class Employee(BaseModel):
	class Role(models.TextChoices):
		ADMIN = 'Admin', _('Admin')
		ACCOUNTANT = 'Accountant', _('Accountant')
		MANAGER = 'Manager', _('Manager')
		FULL_GROOMING = 'Full Grooming', _('Full Grooming')
		WE_WASH = 'We Wash', _('We Wash')

	name = models.CharField(max_length=128,blank=True)
	phone = models.CharField(max_length=16,blank=True)
	email = models.CharField(max_length=64,blank=True)
	role = models.CharField(max_length=16, choices=Role.choices, default=Role.WE_WASH,blank=True)
	branch = models.ForeignKey("scheduling.Branch", on_delete=models.CASCADE, related_name='employees',blank=True,null=True)
	uid = models.CharField(max_length=64,blank=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def is_groomer(self):
		return self.role == self.Role.FULL_GROOMING

	def __str__(self):
		return self.name


