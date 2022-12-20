from django.db import models

from ..common import BaseModel


class Service(BaseModel):
	name = models.CharField(max_length=50)
	description = models.TextField()
	cost = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	duration = models.DurationField()

	def __str__(self):
		return f"{self.name} - {self.description}"
