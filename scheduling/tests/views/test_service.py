from django.test import TestCase
from .mock import services

class ServiceTestCase(TestCase):

	def test_create_service(self):

		response = self.client.post(
			'/api/service',
			services[0],
		)
		self.assertEqual(response.status_code, 201)

		response = self.client.post(
			'/api/service',
			services[1],
		)
		self.assertEqual(response.status_code, 201)


		response = self.client.get('/api/service/1')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['name'], services[0]["name"])
		self.assertEqual(response.data['description'], services[0]["description"])


		response = self.client.patch('/api/service/1',data={
			"name": "New Name",
		},content_type='application/json')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['name'], "New Name")
		self.assertEqual(response.data['description'], services[0]["description"])


		response = self.client.get('/api/services/all')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 2)

	def test_remove_service(self):
		response = self.client.post(
			'/api/service',
			services[0],
		)
		self.assertEqual(response.status_code, 201)
		response = self.client.delete('/api/service/1')
		self.assertEqual(response.status_code, 204)

		response = self.client.get('/api/services/all')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 0)
