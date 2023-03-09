from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from common import BaseModel
from common.roles import Roles


class Employee(BaseModel):


	name = models.CharField(max_length=128,blank=True)
	phone = models.CharField(max_length=32,blank=True)
	email = models.CharField(max_length=64,blank=True)
	role = models.PositiveSmallIntegerField(choices=Roles.CHOICES,default=Roles.EMPLOYEE_WE_WASH)
	branch = models.ForeignKey("scheduling.Branch", on_delete=models.CASCADE, related_name='employees',blank=True,null=True)
	uid = models.CharField(max_length=64,blank=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee',blank=True,null=True)

	def __str__(self):
		return self.name


