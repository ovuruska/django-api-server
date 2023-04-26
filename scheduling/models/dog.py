from django.db import models
from django.utils.translation import gettext_lazy as _

from common import BaseModel


class Dog(BaseModel):
	class CoatType(models.TextChoices):
		SMOOTH_SHORT = 'Smooth - Short'
		SMOOTH_LONG = 'Smooth - Long'
		DOUBLE_COATED = 'Double - Coated'
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
	gender = models.CharField(max_length=6,default="Male")
	coat_type = models.CharField(max_length=20, choices=CoatType.choices, default=CoatType.SMOOTH_LONG)
	birth_date = models.DateField(null=True, blank=True)


	class Meta:
		unique_together = ('owner', 'name')

	def to_dict(self):
		birth_date = self.birth_date.isoformat() if self.birth_date else None
		return {
			"id": self.id,
			"name": self.name,
			"breed": self.breed,
			"age": self.age,
			"weight": self.weight,
			"description": self.description,
			"owner": self.owner.to_dict(),
			"rabies_vaccination": self.rabies_vaccination,
			"employee_notes": self.employee_notes,
			"customer_notes": self.customer_notes,
			"special_handling": self.special_handling,
			"coat_type": self.coat_type,
			"gender":self.gender,
			"birth_date":birth_date,
		}