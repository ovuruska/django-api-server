from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from common.auth_test_case import CustomerAuthTestCase


class VerifyTokenViewTests(CustomerAuthTestCase):
	url = reverse('authorization/verify-token')


	def test_verify_token_valid(self):
		response = self.client.get(self.url,**self.customer_headers)

		self.assertEqual(response.status_code, status.HTTP_200_OK)


	def test_verify_token_empty(self):
		response = self.client.get(self.url)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


	def test_verify_token_invalid(self):
		# Set header
		headers = {
			"HTTP_AUTHORIZATION":"Token invalid_token"
		}

		response = self.client.get(self.url,**headers)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)