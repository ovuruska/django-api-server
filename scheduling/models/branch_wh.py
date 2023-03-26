import datetime

from django.db import models

from common import BaseModel


class BranchWorkingHour(BaseModel):
	week_day = models.IntegerField()
	branch = models.ForeignKey('scheduling.Branch', on_delete=models.CASCADE)
	start = models.DateTimeField(null=True)
	end = models.DateTimeField(null=True)


	class Meta:
		unique_together = ('branch', 'week_day')
