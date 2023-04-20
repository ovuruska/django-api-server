from django.test import TestCase
from django.contrib.auth.models import User
from knox.models import AuthToken

from common.auth_test_case import CustomerAuthTestCase
from common.roles import Roles
from scheduling.models import Employee, Customer, Branch


class TestPetCreateAPIView(CustomerAuthTestCase):
	def test_pet_create_view(self):
		data = {"name": "Buddy", "breed": "Golden Retriever", }
		# Create a dog
		response = self.client.post('/api/dog', data, format='json', content_type="application/json",
		                            **self.customer_headers)
		self.assertEqual(response.status_code, 201)

	def test_create_with_birth_date(self):
		data = {"name": "Buddy", "breed": "Golden Retriever", "birth_date": "2019-01-01"}
		response = self.client.post('/api/dog', data, format='json', content_type="application/json",
		                            **self.customer_headers)
		self.assertEqual(response.status_code, 201)
		response_json = response.json()
		self.assertEqual(response_json["name"], "Buddy")
		self.assertEqual(response_json["breed"], "Golden Retriever")
		self.assertEqual(response_json["birth_date"], "2019-01-01")

