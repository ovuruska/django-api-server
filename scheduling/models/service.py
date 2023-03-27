from django.db import models

from common import BaseModel


class Service(BaseModel):
	name = models.CharField(max_length=50)
	description = models.TextField()
	cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	duration = models.DurationField()

	def __str__(self):
		return f"{self.name} - {self.description}"


	def to_dict(self):
		return {
			"id": self.id,
			"name": self.name,
			"description": self.description,
			"cost": self.cost,
			"duration": self.duration,
			}