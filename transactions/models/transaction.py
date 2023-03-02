from django.db import models
from scheduling.models import Appointment, Employee, Customer
from common import BaseModel

class Transaction(BaseModel):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="appointment")
    employee = models.ForeignKey(Employee, blank=True,on_delete=models.CASCADE, related_name="employee", null=True)
    customer = models.ForeignKey(Customer, blank=True,on_delete=models.CASCADE, related_name="customer", null=True)
    date = models.DateTimeField()
    action = models.CharField(max_length=255)
    description = models.TextField()
