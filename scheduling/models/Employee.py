from django.contrib.auth.models import AbstractUser
from django.db import models
from scheduling.common import BaseModel


class Employee(BaseModel):

	name = models.CharField(max_length=32)
	phone = models.CharField(max_length=32)
	email = models.CharField(max_length=32)
	role = models.CharField(max_length=32)
	branch = models.ForeignKey("scheduling.Branch", on_delete=models.CASCADE, related_name='employees')
	uid = models.CharField(max_length=32)
	# password = models.CharField(max_length=32)
	# username = models.CharField(max_length=32)

	def __str__(self):
		return self.name



