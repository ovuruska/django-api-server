from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator


class EmployeeWorkingHour(models.Model):
	employee = models.ForeignKey('scheduling.Employee', on_delete=models.CASCADE)
	date = models.DateField()

	"""
	0	Monday
	1	Tuesday
	2	Wednesday
	3	Thursday
	4	Friday
	5	Saturday
	6	Sunday
	"""
	week_day = models.IntegerField(defult = 0,validators=[MinValueValidator(0), MaxValueValidator(6)])
	branch = models.ForeignKey('scheduling.Branch', on_delete=models.CASCADE)
	working_hours = models.CharField(max_length=24, validators=[MinLengthValidator(24)],default=24*"0")
