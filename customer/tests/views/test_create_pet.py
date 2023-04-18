
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
			"age": 1,
			"weight": 1,
			"gender":"Male"
		}

		response = self.client.post(self.url, data=data,**self.customer_headers)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(Dog.objects.count(), 1)
		dog_obj = Dog.objects.first()
		self.assertEqual(dog_obj.name, "test")
		self.assertEqual(dog_obj.breed, "test")
		self.assertEqual(dog_obj.age, 1)
		self.assertEqual(dog_obj.weight, 1)
		self.assertEqual(dog_obj.gender,"Male")

	def test_fail_create_same_dog_twice(self):
		data = {
			"name": "test",
			"breed": "test",
			"age": 1,
			"weight": 1,
			"gender": "Male"
		}
		response = self.client.post(self.url, data=data,**self.customer_headers)
		self.assertEqual(response.status_code, 200)
		response = self.client.post(self.url, data=data,**self.customer_headers)
		self.assertEqual(response.status_code, 400)

