import datetime
from datetime import timezone
from time import strptime

from django.apps import apps
from django.urls import reverse
from faker import Faker

from common.auth_test_case import CustomerAuthTestCase

# Get random time from future
faker = Faker()
faker.random.seed(0)
start = faker.future_datetime(end_date="+30d", tzinfo=timezone.utc).replace(hour=12, minute=0, second=0, microsecond=0)

# Path: customer/tests/views/test_appointment.py
Employee = apps.get_model("scheduling", "Employee")
Dog = apps.get_model("scheduling", "Dog")
Product = apps.get_model("scheduling", "Product")
Branch = apps.get_model("scheduling", "Branch")
EmployeeWorkingHours = apps.get_model("scheduling", "EmployeeWorkingHour")

class TestCustomerCreateAppointment(CustomerAuthTestCase):
	url = reverse("customer/appointment/create")
	def setUp(self):
		super().setUp()
		self.dog = Dog.objects.create(name="Dog", breed="Breed", age=1,owner = self.customer)
		self.branch = Branch.objects.create(name="Branch", address="Address")
		self.employee = Employee.objects.create(user=self.user, branch=self.branch)
		self.product = Product.objects.create(name="Product", cost=1)
		week_day = start.weekday()
		EmployeeWorkingHours.objects.create(
			employee=self.employee,
			week_day=week_day,
			branch=self.branch,
			start=datetime.time(9, 0, 0),
			end=datetime.time(16, 0, 0),
		)

	def tearDown(self) -> None:
		super().tearDown()
		self.dog.delete()
		self.branch.delete()
		self.employee.delete()
		self.product.delete()



	def test_create_appointment_grooming(self):
		data = {
			"start": str(start),
			"pet": self.dog.id,
			"branch": self.branch.id,
			"employee": self.employee.id,
			"products": [self.product.id],
			"customer_notes": "Notes",
			"service":"Grooming"
		}
		response = self.client.post(self.url, data=data,format="json",**self.customer_headers)
		response_data = response.json()

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response_data["dog"]["id"], self.dog.id)
		self.assertEqual(response_data["branch"]["id"], self.branch.id)
		self.assertEqual(response_data["employee"]["id"], self.employee.id)
		self.assertEqual(response_data["products"][0]["id"], self.product.id)
		self.assertEqual(response_data["customer_notes"], data["customer_notes"])

	def test_create_appointment_wewash(self ):
		data = {
			"start": str(start),
			"pet": self.dog.id,
			"branch": self.branch.id,
			"employee": self.employee.id,
			"products": [self.product.id],
			"customer_notes": "Notes",
			"service":"We Wash"
		}
		response = self.client.post(self.url, data=data,format="json",**self.customer_headers)
		response_data = response.json()

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response_data["dog"]["id"], self.dog.id)
		self.assertEqual(response_data["branch"]["id"], self.branch.id)
		self.assertEqual(response_data["employee"]["id"], self.employee.id)
		self.assertEqual(response_data["products"][0]["id"], self.product.id)
		self.assertEqual(response_data["customer_notes"], data["customer_notes"])
