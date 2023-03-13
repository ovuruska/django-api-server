from django.db import models
from django.utils.translation import gettext_lazy as _

from common import BaseModel


class Dog(BaseModel):
	class CoatType(models.TextChoices):
		SMOOTH_SHORT = 'SmoothShort'
		SMOOTH_LONG = 'SmoothLong'
		DOUBLE_COATED = 'DoubleCoated'
		DOODLES = 'Doodles'


	name = models.CharField(max_length=32, db_index=True)
	breed = models.CharField(max_length=128)
	age = models.IntegerField(blank=True, null=True)
	weight = models.FloatField(blank=True, null=True)
	description = models.TextField(default="", max_length=200)
	owner = models.ForeignKey("scheduling.Customer", on_delete=models.CASCADE, related_name='dogs')
	rabies_vaccination = models.DateField(null=True, blank=True)
	employee_notes = models.TextField(default="", max_length=1000)
	customer_notes = models.TextField(default="", max_length=1000)
	special_handling = models.BooleanField(default=False)

	coat_type = models.CharField(max_length=20, choices=CoatType.choices, default=CoatType.SMOOTH_LONG)
