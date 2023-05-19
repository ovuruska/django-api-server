"""
import os

from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payment.services.clover import CloverService

CreditCard = apps.get_model('payment.CreditCard')

class DeleteCreditCardView(DeleteView):
	permission_classes = [IsAuthenticated()]

	@swagger_auto_schema(
		responses={204: ''}
	)
	def delete(self, request, *args, **kwargs):
		id = kwargs.get('pk')
		user = request.user
		customer = user.customer
		credit_card = CreditCard.objects.get(id=id, owner=customer)
		clover_service = CloverService()
		clover_service.delete_credit_card(credit_card.customer_token, credit_card.card_token)
		credit_card.delete()

		return Response(status=status.HTTP_204_NO_CONTENT)
"""
"""
	exp_month = models.CharField(max_length=2)
	exp_year = models.CharField(max_length=4)
	first6 = models.CharField(max_length=6)
	last4 = models.CharField(max_length=4)
	brand = models.CharField(max_length=32)
	owner = models.ForeignKey('scheduling.Customer', on_delete=models.CASCADE, related_name='credit_cards')
	customer_token = models.CharField(max_length=100, null=True, blank=True)
	card_token = models.CharField(max_length=100, null=True, blank=True)
"""

from django.apps import apps
from django.urls import reverse
from unittest.mock import patch

from common.auth_test_case import CustomerAuthTestCase


# Path: payment/tests/views/test_delete_credit_card.py

CreditCard = apps.get_model('payment.CreditCard')
Customer = apps.get_model('scheduling.Customer')


class DeleteCreditCardTestCase(CustomerAuthTestCase):
	url = reverse('payment/delete-card')
	credit_card_data = {
		'id':1,
		'exp_month': '01',
		'exp_year': '2025',
		'cvv': '123',
		'first6': '411111',
		'last4': '1111',
		'brand': 'VISA',
		'customer_token': "customer_1234",
		'card_token': "card_1234",
	}

	def test_delete_customer_credit_card(self):
		with patch('payment.models.CreditCard.objects.get', return_value=self.credit_card_data):
			credit_card_id = self.credit_card_data['id']
			self.url
			response = self.client.delete(self.url, **self.customer_headers)
