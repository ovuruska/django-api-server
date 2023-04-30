from datetime import datetime

from django.apps import apps
from django.test import TestCase
from django.urls import reverse

from common.auth_test_case import CustomerAuthTestCase

Dog = apps.get_model("scheduling", "Dog")


class CustomerCreatePetViewTestCase(CustomerAuthTestCase):
	url = reverse("customer/pet/create")

	def test_create_pet_missing_birth_date(self):
		data = {"name": "test_1", "breed": "test", "rabies_vaccination": "2019-01-01", "weight": 1, "gender": "Male"}
		response = self.client.post(self.url, data=data, **self.customer_headers)
		self.assertEqual(response.status_code, 400)

	def test_fail_create_same_dog_twice(self):
		data = {"name": "test_2", "breed": "test", "weight": 1, "birth_date": "2019-01-01", "gender": "Male",
			"special_handling": "", "rabies_vaccination": "2019-01-01", }
		response = self.client.post(self.url, data=data, **self.customer_headers)
		self.assertEqual(response.status_code, 200)
		response = self.client.post(self.url, data=data, **self.customer_headers)
		self.assertEqual(response.status_code, 400)

	def test_create_with_special_handling(self):
		data = {"name": "test_3", "breed": "test", "birth_date": "2019-01-01", "weight": 1, "gender": "Male",
			"special_handling": "test", "rabies_vaccination": "2019-01-01", }
		response = self.client.post(self.url, data=data, **self.customer_headers)



	def test_create_with_special_handling_over_length_1000(self):
		data = {"name": "test_4", "breed": "test", "birth_date": "2019-01-01", "weight": 1, "gender": "Male",
			"special_handling": 1001 * "a", "rabies_vaccination": "2019-01-01", }
		response = self.client.post(self.url, data=data, **self.customer_headers)
		self.assertEqual(response.status_code, 400)

	def test_response(self):
		data = {"name": "test_6", "breed": "Bulldog", "gender": "Male",
		        "birth_date": "2023-03-14T21:00:00.000Z", "special_handling": "", "weight": 51,
		        "rabies_vaccination": "2023-03-14T21:00:00.000Z"}
		response = self.client.post(self.url, data=data, **self.customer_headers)
		self.assertEqual(response.status_code, 200)

	def test_missing_rabies_gives_error(self):
		data = {"name": "test_5", "breed": "Bulldog", "gender": "Male",
		        "birth_date": "2023-03-14T21:00:00.000Z", "special_handling": "", "weight": 51}
		response = self.client.post(self.url, data=data, **self.customer_headers)
		self.assertEqual(response.status_code, 400)
