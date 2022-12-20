from django.test import TestCase
from .mock import products

class ProductTestCase(TestCase):

	def test_remove_product(self):

		response = self.client.post("/api/product",data=products[0],content_type= "application/json")
		self.assertEqual(response.status_code, 201)



		response = self.client.get('/api/product/1')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['name'], products[0]["name"])
		self.assertEqual(response.data['description'], products[0]["description"])


		response = self.client.patch('/api/product/1',data={
			"name": "New Name",
		},content_type='application/json')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['name'], "New Name")
		self.assertEqual(response.data['description'], products[0]["description"])


		response = self.client.delete('/api/product/1')
		self.assertEqual(response.status_code, 204)


		response = self.client.get('/api/products/all')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 0)


	def test_create_multiple_products(self):

		response = self.client.post("/api/product",data=products[0],content_type= "application/json")
		self.assertEqual(response.status_code, 201)

		response = self.client.post("/api/product",data=products[1],content_type= "application/json")
		self.assertEqual(response.status_code, 201)

		response = self.client.get('/api/products/all')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 2)