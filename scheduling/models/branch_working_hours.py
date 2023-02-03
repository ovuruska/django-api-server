from django.db import models

class BranchWorkingHours(models.Model):
	weekday = models.IntegerField()
	branch = models.ForeignKey('branches.Branch', on_delete=models.CASCADE)
	start = models.TimeField()
	end = models.TimeField()
