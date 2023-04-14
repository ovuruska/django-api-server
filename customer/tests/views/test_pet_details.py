from django.urls import reverse

from common.auth_test_case import CustomerAuthTestCase
from customer.tests.views.generate_utils import generate_customer_dogs_with_appointments


class GetCustomerPetDetailsTestCase(CustomerAuthTestCase):
	url = reverse("customer/pets/all")
	def setUp(self) -> None:
		super().setUp()
		generate_customer_dogs_with_appointments(self.customer)

	def test_get_customer_pet_details_unauthorized(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 401)

	def test_get_customer_pet_details(self):
		response = self.client.get(self.url, **self.customer_headers)
		self.assertEqual(response.status_code, 200)
		response_data = response.json()
		self.assertEqual(len(response_data), 5)
		for dog in response_data:
			self.assertIsNotNone(dog.get("number_of_wewashes",None))
			self.assertIsNotNone(dog.get("number_of_groomings",None))

	def test_get_customer_pet_details_no_dogs(self):
		self.customer.dogs.all().delete()
		response = self.client.get(self.url, **self.customer_headers)
		self.assertEqual(response.status_code, 200)
		response_data = response.json()
		self.assertEqual(len(response_data), 0)

	def test_get_customer_pet_details_one_dog_only_we_wash(self):
		self.customer.dogs.all().delete()
		generate_customer_dogs_with_appointments(self.customer, appointment_types=["We Wash"])
		response = self.client.get(self.url, **self.customer_headers)
		self.assertEqual(response.status_code, 200)
		response_data = response.json()
		self.assertEqual(len(response_data), 5)
		for dog in response_data:
			self.assertIsNotNone(dog.get("number_of_wewashes",None))
			self.assertEqual(dog.get("number_of_groomings",None), 0)


	def test_get_customer_pet_details_ond_dog_only_grooming(self):
		self.customer.dogs.all().delete()
		generate_customer_dogs_with_appointments(self.customer, appointment_types=["Full Grooming"])
		response = self.client.get(self.url, **self.customer_headers)
		self.assertEqual(response.status_code, 200)
		response_data = response.json()
		self.assertEqual(len(response_data), 5)
		for dog in response_data:
			self.assertEqual(dog.get("number_of_wewashes",None), 0)
			self.assertIsNotNone(dog.get("number_of_groomings",None))