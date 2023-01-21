from django.test import TestCase

from scheduling.models import Employee, Customer, Dog, Branch, Service, Product
from ..mock import *


class AppointmentCRUDTestCase(TestCase):
	"""
		Tests if the appointment can be updated

	"""

	def setUp(self) -> None:
		Customer.objects.create(
			**customers[0]
		)
		Dog.objects.create(
			**dogs[0],
			owner=Customer.objects.get(id=1)
		)
		Branch.objects.create(
			**branches[0]
		)
		Employee.objects.create(
			**employees[0],
			branch=Branch.objects.get(id=1)
		)
		for service in services:
			Service.objects.create(
				**service
			)

		for product in products:
			Product.objects.create(
				**product
			)

	def test_create_appointment_without_product(self):
		response = self.client.post("/api/appointment", {
			"customer": customers[0]["uid"],
			"branch": 1,
			"dog": 1,
			"customer_notes": "Hello world!",
			"start": "2020-12-12T12:00:00Z",
			"services": [1],
			"products": []
		}, content_type="application/json")

		self.assertEqual(response.status_code, 201)

		response = self.client.get("/api/appointment/1")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data["products"], [])

		response = self.client.get(f"/api/appointments/{customers[0]['uid']}")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 1)
		self.assertEqual(response.data[0]["products"], [])

	def test_create_appointment_with_dog_name(self):
		response = self.client.post("/api/appointment", {
			"customer": customers[0]["uid"],
			"branch": 1,
			"dog": dogs[0]["name"],
			"customer_notes": "Hello world!",
			"start": "2020-12-12T14:00:00Z",
			"services": [1],
			"products": []
		}, content_type="application/json")

		self.assertEqual(response.status_code, 201)

		response = self.client.get("/api/appointment/1")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data["products"], [])

		response = self.client.get(f"/api/appointments/{customers[0]['uid']}")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 1)
		self.assertEqual(response.data[0]["products"], [])

	def test_appointment_cannot_be_created_if_busy(self):
		response = self.client.post("/api/appointment", {
			"customer": customers[0]["uid"],
			"branch": 1,
			"dog": dogs[0]["id"],
			"customer_notes": "Hello world!",
			"start": "2020-12-12T14:00:00Z",
			"services": [1],
			"products": []
		}, content_type="application/json")

		self.assertEqual(response.status_code, 201)

		response = self.client.post("/api/appointment", {
			"customer": customers[0]["uid"],
			"branch": 1,
			"dog": dogs[0]["name"],
			"customer_notes": "Hello world!",
			"start": "2020-12-12T14:00:00Z",
			"services": [1],
			"products": []
		}, content_type="application/json")

		self.assertEqual(response.status_code, 400)
		self.assertNotEqual(response.data["error"], None)

	def test_fetch(self):
		response = self.client.post("/api/appointment", {
			"customer": customers[0]["uid"],
			"branch": 1,
			"dog": dogs[0]["name"],
			"customer_notes": "Hello world!",
			"start": "2020-12-12T14:00:00Z",
			"services": [1],
			"products": []
		}, content_type="application/json")

		self.assertEqual(response.status_code, 201)

		response = self.client.get("/api/appointment/1")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data["products"], [])
		self.assertEqual(response.data["customer"]["name"], customers[0]["name"])

		self.assertEqual(response.data["dog"]["name"], dogs[0]["name"])
