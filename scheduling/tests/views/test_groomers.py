from .mock import branches
from .mock import employees
from django.test import TestCase

from ...models import Branch, Employee


class GroomerTestCase(TestCase):
	def setUp(self):
		"""
		Setup the test case
		"""
		for branch in branches:
			Branch.objects.create(**branch)

	def test_create_groomer(self):
		# Create employee with no branch
		employee = employees[0]
		employee["branch"] = 1
		employee["role"] = "Full Grooming"
		result = self.client.post('/api/employee', data=employee, content_type="application/json")
		self.assertEqual(result.status_code, 201)

	def test_retrieve_groomers(self):
		employee = employees[0]
		employee["branch"] = 1
		employee["role"] = "Full Grooming"
		self.client.post('/api/employee', data=employee, content_type="application/json")

		employee = employees[1]
		employee["branch"] = 1
		employee["role"] = "Full Grooming"
		self.client.post('/api/employee', data=employee, content_type="application/json")

		employee = employees[2]
		employee["branch"] = 1
		employee["role"] = "We Wash"
		self.client.post('/api/employee', data=employee, content_type="application/json")

		result = self.client.get('/api/employee/groomers')
		self.assertEqual(result.status_code, 200)
		self.assertEqual(len(result.data), 2)


	def test_create_error_with_wrong_field(self):
		employee = employees[0]
		employee["branch"] = 1
		employee["role"] = "Wrong field"
		response = self.client.post('/api/employee', data=employee, content_type="application/json")
		self.assertEqual(response.status_code, 400)

