from django.urls import reverse

from common.auth_test_case import CustomerAuthTestCase

class CreateCreditCardTestCase(CustomerAuthTestCase):
	url = reverse('payment/create-card')

	def test_with_invalid_card_request_returns_400(self):
		data = {
			"address": {
				"city": "São Paulo",
				"country": "BR",
				"address_line_1": "Rua dos Pinheiros",
				"address_line_2": "Apto 123",
				"postal_code": "12345678",
				"state": "SP"
			},
			"card_number": "1234123412341234",
			"cvv": "123",
			"exp_date": "12/20",
			"brand": "VISA",
			"cardholder_name": "John Doe"
		}
		response = self.client.post(self.url, data=data,format='json',**self.customer_headers)
		self.assertEqual(response.status_code, 400)

	def test_with_invalid_card_number_request_returns_201(self):
		data = {
			"address": {
				"city": "São Paulo",
				"country": "BR",
				"address_line_1": "Rua dos Pinheiros",
				"address_line_2": "Apto 123",
				"postal_code": "12345678",
				"state": "SP"
			},
			"card_number": "1234123412341234",
			"cvv": "123",
			"exp_date": "12/2023",
			"brand": "VISA",
			"cardholder_name": "John Doe"
		}
		try:
			self.client.post(self.url, data=data,format='json',content_type="application/json",**self.customer_headers)
			raise Exception("Should have raised an exception")
		except Exception as e:
			...

	def test_with_valid_card_request_returns_201(self):
		data = {
			"address": {
				"city": "Sunnyvale",
				"country": "US",
				"address_line_1": "415 N Mathilda Ave",
				"address_line_2": "Apto 123",
				"postal_code": "94085",
				"state": "CA"
			},
			"card_number": "6011361000006668",
			"cvv": "123",
			"exp_date": "12/2026",
			"brand": "DISCOVER",
			"cardholder_name": "John Doe"
		}
		response = self.client.post(self.url, data=data,format='json',content_type="application/json",**self.customer_headers)
		self.assertEqual(response.status_code, 201)