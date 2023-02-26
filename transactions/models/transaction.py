from common import BaseModel
from django.db import models
from scheduling.models import Appointment, Employee


class Transaction(BaseModel):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="appointment")
    employee = models.ForeignKey(Employee, blank=True,on_delete=models.CASCADE, related_name="employee")
    date = models.DateTimeField()
    action = models.CharField(max_length=255)
    description = models.TextField()
