from ..common import BaseModel
from django.db import models

class Service(BaseModel):
	name = models.CharField(max_length=50)
	description = models.TextField()
	price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	duration = models.DurationField()

	def __str__(self):
		return self.name