from django.contrib.auth.models import User
from django.db import models
from common import BaseModel
from common.roles import Roles


class Customer(BaseModel):

	name = models.CharField(max_length=64,db_index=True)
	uid = models.CharField(max_length=128)
	email = models.EmailField()
	phone = models.CharField(max_length=32)
	address = models.CharField(max_length=128)
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True)
	role = models.PositiveSmallIntegerField(choices=Roles.CHOICES,default=Roles.CUSTOMER)
	validated = models.BooleanField(default=True)
	class Meta:
		ordering = ["name"]
