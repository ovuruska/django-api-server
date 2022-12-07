from django.db import models
from ..common import BaseModel


class Customer(BaseModel):
	name = models.CharField(max_length=64)
	uid = models.CharField(max_length=128)
	email = models.EmailField()
	phone = models.CharField(max_length=32)
	address = models.CharField(max_length=128)

	class Meta:
		ordering = ["name","email"]