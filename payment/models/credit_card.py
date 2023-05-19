from django.db import models
from common import BaseModel


class CreditCard(BaseModel):

	exp_month = models.CharField(max_length=2)
	exp_year = models.CharField(max_length=4)
	first6 = models.CharField(max_length=6)
	last4 = models.CharField(max_length=4)
	brand = models.CharField(max_length=32)
	owner = models.ForeignKey('scheduling.Customer', on_delete=models.CASCADE, related_name='credit_cards')
	customer_token = models.CharField(max_length=100, null=True, blank=True)
	card_token = models.CharField(max_length=100, null=True, blank=True)

	class Meta:
		db_table = 'credit_card'
		verbose_name = 'Credit Card'
		verbose_name_plural = 'Credit Cards'
		indexes = [
			models.Index(fields=['owner_id'])
		]