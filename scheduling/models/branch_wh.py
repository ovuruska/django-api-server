import datetime

from django.db import models


class BranchWorkingHour(models.Model):
	week_day = models.IntegerField()
	date = models.DateField(default=datetime.date.today)
	branch = models.ForeignKey('scheduling.Branch', on_delete=models.CASCADE)
	start = models.DateTimeField(null=True)
	end = models.DateTimeField(null=True)


	class Meta:
		unique_together = ('branch', 'date')
