from django.db import models
from ..common import BaseModel


class Customer(BaseModel):
	first_name = models.CharField(max_length=32)
	last_name = models.CharField(max_length=32)
	email = models.EmailField()
	phone = models.CharField(max_length=32)
	address = models.CharField(max_length=128)
	zip_code = models.CharField(max_length=5)
	dogs = models.ManyToManyField("Dog", related_name="owners")