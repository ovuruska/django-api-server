from unittest.mock import patch

from django.urls import reverse
from common.auth_test_case import CustomerAuthTestCase

class CreateCreditCardTestCase(CustomerAuthTestCase):
	url = reverse('payment/create-card')
	credit_card_information = {"address": {"city": "Sunnyvale", "country": "US", "address_line_1": "415 N Mathilda Ave",
	                                       "address_line_2": "Apto 123", "postal_code": "94085", "state": "CA"},
	                           "card_number": "6011361000006668", "cvv": "123", "exp_date": "12/2026",
	                           "brand": "DISCOVER", "cardholder_name": "John Doe"}

	credit_card_response = {"exp_month": "12", "exp_year": "2026", "cvv": "123", "first6": "601136", "last4": "6668",
		"brand": "DISCOVER", "card_token": "card_1234", "customer_token": "customer_1234"}

	@patch('payment.services.clover.CloverService.__init__', return_value=None)
	@patch('payment.services.clover.CloverService.create_credit_card', return_value={})
	def test_with_invalid_card_number_request_returns_400(self, _,__):
		data = {**self.credit_card_information, 'card_number': 'invalid'}
		response = self.client.post(self.url, data=data, format='json', **self.customer_headers)
		self.assertEqual(response.status_code, 400)

	@patch('payment.services.clover.CloverService.__init__', return_value=None)
	@patch('payment.services.clover.CloverService.create_credit_card', return_value={})
	def test_with_invalid_card_number_request_returns_400(self, _,__):
		data = {**self.credit_card_information, 'cvv': '1234'}
		response = self.client.post(self.url, data=data, format='json', **self.customer_headers)
		self.assertEqual(response.status_code, 400)

	@patch('payment.services.clover.CloverService.__init__', return_value=None)
	@patch('payment.services.clover.CloverService.create_credit_card', return_value={})
	def test_with_invalid_card_number_request_returns_400(self, _,__):
		data = {**self.credit_card_information, 'exp_date': '12/2020'}
		response = self.client.post(self.url, data=data, format='json', **self.customer_headers)
		self.assertEqual(response.status_code, 400)

	@patch('payment.services.clover.CloverService.__init__', return_value=None)
	@patch('payment.services.clover.CloverService.create_credit_card', return_value={})
	def test_with_invalid_card_number_request_returns_400(self, _,__):
		data = {**self.credit_card_information, 'exp_date': 'invalid'}
		response = self.client.post(self.url, data=data, format='json', **self.customer_headers)
		self.assertEqual(response.status_code, 400)

	@patch('payment.services.clover.CloverService.__init__', return_value=None)
	@patch('payment.services.clover.CloverService.create_credit_card', return_value=credit_card_response)
	def test_with_valid_card_request_returns_201(self, mock_create_credit_card,mock_clover_service_init):
		data = self.credit_card_information
		response = self.client.post(self.url, data=data, format='json', content_type="application/json",
		                            **self.customer_headers)
		self.assertEqual(response.status_code, 201)
		response_data = response.json()
		self.assertIsNotNone(response_data['id'])
		self.assertIsNone(response_data.get('card_token',None))
		self.assertIsNone(response_data.get('customer_token',None))
		self.assertEqual(response_data['brand'], self.credit_card_response['brand'])
		self.assertEqual(response_data['exp_month'], self.credit_card_response['exp_month'])
		self.assertEqual(response_data['exp_year'], self.credit_card_response['exp_year'])
		self.assertEqual(response_data['first6'], self.credit_card_response['first6'])
		self.assertEqual(response_data['last4'], self.credit_card_response['last4'])
		mock_create_credit_card.assert_called_once()
		mock_clover_service_init.assert_called_once()

	@patch('payment.services.clover.CloverService.__init__', return_value=None)
	@patch('payment.services.clover.CloverService.create_credit_card', return_value=credit_card_response)
	def test_allow_address_line_2_is_blank(self, _,__):
		data = {
			**self.credit_card_information,
		}
		data['address']['address_line_2'] = ''
		response = self.client.post(self.url, data=data, format='json', content_type="application/json",
		                            **self.customer_headers)
		self.assertEqual(response.status_code, 201)

	@patch('payment.services.clover.CloverService.__init__', return_value=None)
	@patch('payment.services.clover.CloverService.create_credit_card', return_value=credit_card_response)
	def test_allow_address_line_2_is_empty(self,_,__):
		data = {
			**self.credit_card_information,
		}
		del data['address']['address_line_2']
		response = self.client.post(self.url, data=data, format='json', content_type="application/json",
		                            **self.customer_headers)
		self.assertEqual(response.status_code, 201)
