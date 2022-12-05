from django.db import models

from ..common import BaseModel


class Dog(BaseModel):
	name = models.CharField(max_length=32)
	breed = models.CharField(max_length=128)
	age = models.IntegerField()
	weight = models.FloatField()
