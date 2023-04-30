from datetime import datetime

from django.apps import apps
from django.test import TestCase
from django.urls import reverse

from common.auth_test_case import CustomerAuthTestCase
Dog = apps.get_model("scheduling", "Dog")

class CustomerCreatePetViewTestCase(CustomerAuthTestCase):
	url = reverse("customer/pet/create")

	def test_create_pet(self):
		data = {
			"name": "test",
			"breed": "test",
			"birth_date": "2019-01-01",
			"weight": 1,
			"gender":"Male"
		}
		response = self.client.post(self.url, data=data,**self.customer_headers)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(Dog.objects.count(), 1)
		dog_obj = Dog.objects.first()
		self.assertEqual(dog_obj.name, "test")
		self.assertEqual(dog_obj.breed, "test")
		self.assertIsNotNone(dog_obj.birth_date)
		self.assertEqual(dog_obj.weight, 1)
		self.assertEqual(dog_obj.gender,"Male")

	def test_fail_create_same_dog_twice(self):
		data = {
			"name": "test",
			"breed": "test",
			"weight": 1,
			"birth_date": "2019-01-01",
			"gender": "Male"
		}
		response = self.client.post(self.url, data=data,**self.customer_headers)
		self.assertEqual(response.status_code, 200)
		response = self.client.post(self.url, data=data,**self.customer_headers)
		self.assertEqual(response.status_code, 400)


	def test_create_with_special_handling(self):
		data = {
			"name": "test",
			"breed": "test",
			"birth_date": "2019-01-01",
			"weight": 1,
			"gender": "Male",
			"special_handling": "test"
		}
		response = self.client.post(self.url, data=data,**self.customer_headers)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(Dog.objects.count(), 1)
		dog_obj = Dog.objects.first()
		self.assertEqual(dog_obj.name, "test")
		self.assertEqual(dog_obj.breed, "test")
		self.assertIsNotNone(dog_obj.birth_date)
		self.assertEqual(dog_obj.weight, 1)
		self.assertEqual(dog_obj.gender,"Male")
		self.assertEqual(dog_obj.customer_notes, "test")

	def test_create_with_special_handling_over_length_1000(self):
		data = {
			"name": "test",
			"breed": "test",
			"birth_date": "2019-01-01",
			"weight": 1,
			"gender": "Male",
			"special_handling": 1001* "a"
		}
		response = self.client.post(self.url, data=data,**self.customer_headers)
		self.assertEqual(response.status_code, 400)



	def test_response(self):
		data = {"name":"Oğuz Vuruşkaner","breed":"Bulldog","gender":"Male","birth_date":"2023-03-14T21:00:00.000Z","special_handling":"","weight":51}
		response = self.client.post(self.url, data=data,**self.customer_headers)
		self.assertEqual(response.status_code, 200)


	def test_response_2(self):
		data = {"name":"Johnnie","breed":"German Shepherd","gender":"Male","birth_date":"2023-04-30T11:15:21.908Z","special_handling":"","weight":21,"rabies_vaccination":"2023-04-30T11:15:21.908Z"}
		response = self.client.post(self.url, data=data,**self.customer_headers)
		self.assertEqual(response.status_code, 200)
		data = {"name":"Johnnie","breed":"German Shepherd","gender":"Male","birth_date":"2023-04-30T11:15:21.908Z","special_handling":"","weight":21,"rabies_vaccination":"2023-04-30T11:15:21.908Z"}
		response = self.client.post(self.url, data=data,**self.customer_headers)
		self.assertEqual(response.status_code, 400)

