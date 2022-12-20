from datetime import datetime, timedelta

from django.test import TestCase

from scheduling.models import Branch, Employee, Customer, Dog, Appointment
from scheduling.tests.views.mock import branches, employees, customers, dogs


class AppointmentStatusTestCase(TestCase):
	"""

	"""

	test_url = "/appointment/1"

	def setUp(self):
		for branch in branches:
			Branch.objects.create(
				**branch
			)

		for employee in employees:
			Employee.objects.create(
				branch=Branch.objects.get(id=1),
				**employee
			)
		for customer in customers:
			Customer.objects.create(
				**customer
			)
		for dog in dogs:
			Dog.objects.create(
				owner=Customer.objects.get(id=1),
				**dog
			)

	def create_appointment(self):
		Appointment.objects.create(
			customer=Customer.objects.get(id=1),
			dog=Dog.objects.get(id=1),
			start=datetime.now(),
			end=datetime.now() + timedelta(hours=1),
			customer_notes="Hello world!",
			employee_notes="Hello world!",
			branch=Branch.objects.get(id=1),
			employee=Employee.objects.get(id=1),
		)

	def test_set_appointment_status(self):

		self.create_appointment()

		response = self.client.patch("/api/schedule/appointment/1",{
			"status":"Cancelled"
		},content_type="application/json")
		print(response.data)
		self.assertEqual(response.status_code, 200)

		response = self.client.get("/api/appointment/1")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data["status"], "Cancelled")

	def test_set_appointment_status_with_invalid_status(self):

		self.create_appointment()

		response = self.client.patch("/api/schedule/appointment/1",{
			"status":"INVALID"
		},content_type="application/json")
		self.assertEqual(response.status_code, 400)

	def test_set_appointment_status_after_completed(self):

		self.create_appointment()

		response = self.client.patch("/api/schedule/appointment/1", {
			"status": "Completed"
		}, content_type="application/json")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data["status"], "Completed")

		response = self.client.patch("/api/schedule/appointment/1", {
			"status": "Pending"
		}, content_type="application/json")
		self.assertEqual(response.status_code, 400)

		response = self.client.get("/api/appointment/1")
		self.assertEqual(response.data["status"], "Completed")

