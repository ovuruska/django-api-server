from django.contrib.auth.models import User
from django.db import models
from common import BaseModel


class Customer(BaseModel):
	name = models.CharField(max_length=64)
	uid = models.CharField(max_length=128)
	email = models.EmailField()
	phone = models.CharField(max_length=32)
	address = models.CharField(max_length=128)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	class Meta:
		ordering = ["name"]
