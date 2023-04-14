"""
from rest_framework import generics

from customer.selectors.pet_details import get_customer_pet_details
from customer.serializers.responses.pet_details import CustomerPetDetailsResponseSerializer


class GetCustomerPetDetails(generics.ListAPIView):

	serializer_class = CustomerPetDetailsResponseSerializer

	def get_queryset(self):
		customer = self.request.user.customer
		return get_customer_pet_details(customer)


"""
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
