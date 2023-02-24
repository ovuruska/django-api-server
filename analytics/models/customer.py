from django.db import models

from common import BaseModel


class TopCustomer(BaseModel):
	customer = models.ForeignKey("scheduling.customer", on_delete=models.CASCADE)
	total_tips = models.DecimalField(max_digits=10, decimal_places=2)
	total_product_invoices = models.DecimalField(max_digits=10, decimal_places=2)
	total_service_invoices = models.DecimalField(max_digits=10, decimal_places=2)
	last_appointment_date = models.DateTimeField(default=None, null=True)

	class Meta:
		managed = False
		db_table = 'top_customer'
