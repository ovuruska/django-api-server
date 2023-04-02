from django.urls import reverse
from rest_framework import status

from common.auth_test_case import CustomerAuthTestCase


class CustomerRegisterViewTest(CustomerAuthTestCase):
	url = reverse('authorization/customer-register')

	def test_register_customer_valid(self):
		# Set data
		data = {
			"username": "oguz@gmail.com",
			"password": "testpassword",

		}
		response = self.client.post(self.url, data=data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_existing_customer_fails(self):
		# Set data
		data = {
			"username": self.customer_username,
			"password": self.customer_password,

		}
		response = self.client.post(self.url, data=data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_empty_fields_fail(self):
		# Set data
		data = {
			"username": "",
			"password": "",

		}
		response = self.client.post(self.url, data=data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

