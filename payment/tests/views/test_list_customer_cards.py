"""
from django.apps import apps
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.serializers.models.credit_card import CreditCardSerializer

CreditCard = apps.get_model('payment.CreditCard')

class ListCustomerCardsView(APIView):
	def get(self, request, *args, **kwargs):
		user = request.user
		customer = user.customer
		cards = CreditCard.objects.find(owner=customer)
		serializer = CreditCardSerializer(cards, many=True)
		return Response(serializer.data)
"""
from django.apps import apps
from django.urls import reverse

from common.auth_test_case import CustomerAuthTestCase

CreditCard = apps.get_model('payment.CreditCard')

class ListCustomerCardsViewTestCase(CustomerAuthTestCase):
	url = reverse('payment/list-cards')
	def setUp(self):
		super().setUp()
		self.credit_card = CreditCard.objects.create(
			exp_month='01',
			exp_year='2020',
			first6='123456',
			last4='7890',
			brand='VISA',
			owner=self.customer,
			customer_token='customer_token',
			card_token='card_token'
		)

	def test_list_customer_cards(self):
		response = self.client.get(self.url, **self.customer_headers)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 1)
		self.assertEqual(response.data[0]['id'], self.credit_card.id)
		self.assertEqual(response.data[0]['exp_month'], self.credit_card.exp_month)
		self.assertEqual(response.data[0]['exp_year'], self.credit_card.exp_year)
		self.assertEqual(response.data[0]['first6'], self.credit_card.first6)
		self.assertEqual(response.data[0]['last4'], self.credit_card.last4)
		self.assertEqual(response.data[0]['brand'], self.credit_card.brand)
		self.assertEqual(response.data[0].get("customer_token",None), None)
		self.assertEqual(response.data[0].get("card_token",None), None)
		self.assertEqual(response.data[0].get("owner"), None)

	def test_list_customer_cards_unauthenticated(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 401)
		self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')