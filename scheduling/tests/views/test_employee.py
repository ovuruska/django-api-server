from django.test import TestCase

from scheduling.models import Branch
from .mock import branches
from .mock import employees

class EmployeeTestCase(TestCase):

	def setUp(self):
		for branch in branches:
			Branch.objects.create(**branch)

	def test_create_employee(self):
		# Create employee with no branch
		employee = employees[0]
		employee["branch"] = 1
		employee["role"] = "Full Grooming"
		result = self.client.post('/api/employee', data=employee,content_type="application/json")

		self.assertEqual(result.status_code, 201)


	def test_remove_employee(self):
		employee = employees[0]
		employee["branch"] = 1
		employee["role"] = "Full Grooming"

		self.client.post('/api/employee', data=employee, content_type="application/json")
		result = self.client.delete('/api/employee/1')

		self.assertEqual(result.status_code, 204)

		result = self.client.get('/api/employee', data=employee, content_type="application/json")
		self.assertEqual(result.status_code, 405)


	def test_modify_and_employee(self):
		employee = employees[0]
		employee["branch"] = 1
		self.client.post('/api/employee', data=employee, content_type="application/json")
		self.client.patch('/api/employee/1', data={"name": "Robert Paulsen"}, content_type="application/json")

		result = self.client.get("/api/employee/1")
		self.assertEqual(result.status_code, 200)
		self.assertEqual(result.data["name"], "Robert Paulsen")



