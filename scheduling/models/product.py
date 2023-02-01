from django.db import models

from common import BaseModel


class Product(BaseModel):
	name = models.CharField(max_length=50)
	description = models.TextField()
	cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	category = models.CharField(max_length=50, default="Other")
	def __str__(self):
		return f"{self.name} - {self.description}"
