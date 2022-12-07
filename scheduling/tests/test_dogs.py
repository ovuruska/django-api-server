from django.test import TestCase

from scheduling.models import Customer

from mock import customers as customers
from mock import dogs as test_dogs






class DogsTestCase(TestCase):

	def setUp(self) -> None:
		Customer.objects.create(**customers[0])
		Customer.objects.create(**customers[1])


	def add_dog(self,dog,user_id):
		dog['owner'] = user_id
		response = self.client.post('/api/dog', data=dog)
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

