from django.db import models
import datetime


class BranchWorkingHour(models.Model):
    weekday = models.IntegerField()
    date = models.DateField(default=datetime.date.today)
    branch = models.ForeignKey('scheduling.Branch', on_delete=models.CASCADE)
    workingHours = models.CharField(max_length=24,default="000000000000000000000000",blank=True)

    class Meta:
        unique_together = ('branch', 'date')