from django.test import TestCase

from scheduling.models import Customer

from .mock import customers as customers
from .mock import dogs as test_dogs






class DogsTestCase(TestCase):

	def setUp(self) -> None:
		Customer.objects.create(**customers[0])
		Customer.objects.create(**customers[1])


	def add_dog(self,dog,user_id):
		dog['owner'] = user_id
		response = self.client.post()
		return response


	def test_add_remove_dog(self):
		uid = customers[0]['uid']
		response = self.add_dog(test_dogs[0],uid)
		self.assertEqual(response.status_code, 201)
		dog_id = response.data.pop('id')
		response = self.client.get(f'/api/dog/{dog_id}')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['name'], test_dogs[0]['name'])

		response = self.client.delete(f'/api/dog/{dog_id}')
		self.assertEqual(response.status_code, 204)

	def test_list_dogs(self):
		uid = customers[0]['uid']
		for dog in test_dogs:
			self.add_dog(dog,uid)
		response = self.client.get(f'/api/dogs/{uid}')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), len(test_dogs))

		for dog in response.data:
			self.client.delete(f'/api/dog/{dog["id"]}')

		response = self.client.get(f'/api/dogs/{uid}')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 0)

	def test_modify_dogs(self):
		uid = customers[0]['uid']
		for dog in test_dogs:
			self.add_dog(dog,uid),

		response = self.client.get(f'/api/dogs/{uid}')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), len(test_dogs))
		first_dog = response.data[0]
		first_dog['name'] = 'new name'
		response = self.client.patch(f'/api/dog/{first_dog["id"]}', data={
			"name":first_dog['name']
		}, content_type="application/json")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['name'], 'new name')
		response = self.client.get(f'/api/dog/{first_dog["id"]}')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['name'], 'new name')