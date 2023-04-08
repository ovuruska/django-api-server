from django.db import models

from common import BaseModel


class Product(BaseModel):
	name = models.CharField(max_length=50)
	description = models.TextField()
	cost = models.FloatField(default=0.00)
	category = models.CharField(max_length=100, default="Other")
	sub_category = models.CharField(max_length=100, default="Other")
	def __str__(self):
		return f"{self.name} - {self.description}"

	def to_dict(self):
		return {
			"id": self.id,
			"name": self.name,
			"description": self.description,
			"cost": self.cost,
			"category": self.category,
			"sub_category": self.sub_category,
		}