from datetime import timezone, timedelta

from django.apps import apps
# Path: customer/tests/views/test_appointment_cancel.py

from django.test import TestCase
from django.urls import reverse
from faker import Faker

from common.auth_test_case import CustomerAuthTestCase

# Get random time from future
faker = Faker()
faker.random.seed(0)
start = faker.future_datetime(end_date="+30d", tzinfo=timezone.utc).replace(hour=12, minute=0, second=0, microsecond=0) + timedelta(hours=48)

# Path: customer/tests/views/test_appointment.py
Employee = apps.get_model("scheduling", "Employee")
Dog = apps.get_model("scheduling", "Dog")
Product = apps.get_model("scheduling", "Product")
Branch = apps.get_model("scheduling", "Branch")
Appointment = apps.get_model("scheduling", "Appointment")
Customer = apps.get_model("scheduling", "Customer")


class CustomerCancelAppointmentTest(CustomerAuthTestCase):
	url = reverse("customer/appointment/cancel", kwargs={"appointment_id": 1})
	def setUp(self):
		super().setUp()
		self.branch = Branch.objects.create(name="Test Branch")
		self.employee = Employee.objects.create(name="Test Employee", branch=self.branch)
		self.dog = Dog.objects.create(name="Test Dog", owner=self.customer)

		self.appointment = Appointment.objects.create(
			customer=self.customer,
			employee=self.employee,
			start=start,
			appointment_type="We Wash",
			branch=self.branch,
			end=start + timedelta(minutes=90),
			customer_notes="",
			dog=self.dog,
			status="Confirmed"
		)

	def test_cancel_appointment(self):

		response = self.client.put(self.url, format="json",**self.customer_headers)
		self.assertEqual(response.status_code, 200)
		upd_appt = Appointment.objects.get(id=1)
		self.assertEqual(upd_appt.status, "Cancelled")

	def test_cancel_appointment_not_found(self):
		self.url = reverse("customer/appointment/cancel", kwargs={"appointment_id": 2})
		response = self.client.put(self.url, format="json",**self.customer_headers)
		self.assertEqual(response.status_code, 404)

	def test_cancel_appointment_not_customer(self):
		other_customer = Customer.objects.create(
			email=""
		)
		other_dog = Dog.objects.create(name="Test Dog", owner=other_customer)
		Appointment.objects.create(
			customer=other_customer,
			employee=self.employee,
			start=start,
			dog=other_dog,
			appointment_type="We Wash",
			branch=self.branch
		)
		url = reverse("customer/appointment/cancel", kwargs={"appointment_id": 2})

		response = self.client.put(url, format="json",**self.customer_headers)
		self.assertEqual(response.status_code, 404)