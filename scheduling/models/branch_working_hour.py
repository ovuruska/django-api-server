from django.db import models


class BranchWorkingHour(models.Model):
    weekday = models.IntegerField()
    branch = models.ForeignKey('scheduling.Branch', on_delete=models.CASCADE)
    workingHours = models.CharField(max_length=24,default="000000000000000000000000",blank=True)
