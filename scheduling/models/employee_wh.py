import datetime

from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from common import BaseModel


class EmployeeWorkingHour(BaseModel):
	"""
	EmployeeWorkingHour model

	0	Monday
	1	Tuesday
	2	Wednesday
	3	Thursday
	4	Friday
	5	Saturday
	6	Sunday
	"""
	employee = models.ForeignKey('scheduling.Employee', on_delete=models.CASCADE)
	week_day = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
	branch = models.ForeignKey('scheduling.Branch', on_delete=models.CASCADE)
	start = models.TimeField(null=True)
	end = models.TimeField(null=True)
	class Meta:
		unique_together = ('employee', 'week_day')
		ordering = ('-start',)