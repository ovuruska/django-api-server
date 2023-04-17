"""class CustomerCreatePetView(generics.CreateAPIView):
	serializer_class = CustomerPetDetailsResponseSerializer

	@validate_request(CreatePetRequestSerializer)
	def create(self, request, *args, **kwargs):
		serialized_data = kwargs.get("serialized_data")
		customer = request.user.customer
		pet_name = serialized_data.get("name")
		pet = Dog.objects.create(owner=customer, name=pet_name, breed=serialized_data.get("breed"),
			age=serialized_data.get("age"), weight=serialized_data.get("weight"), gender=serialized_data.get("gender"))
		pet_details = get_customer_pet_details(customer, pet_name)

		serializer = CustomerPetDetailsResponseSerializer(pet_details)

		return Response(serializer.data)
"""
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

