from django.db import models


class BranchWorkingHour(models.Model):
    weekday = models.IntegerField()
    branch = models.ForeignKey('scheduling.Branch', on_delete=models.CASCADE)
    workingHours  = models.CharField(max_length=24,default="000000000000000000000000",blank=True)

    def clean(self):
        existing_hours = workingHours.objects.filter(
            branch=self.branch, weekDay=self.weekDay
        )
        for hours in existing_hours:
            # check for overlap with existing working hours
            if (
                    self.start_time >= hours.start_time
                    and self.start_time < hours.end_time
            ) or (
                    self.end_time > hours.start_time
                    and self.end_time <= hours.end_time
            ):
                hours.delete()
        super().clean()
