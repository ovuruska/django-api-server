from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from scheduling.models import Appointment, Customer, Dog, Product, Service, Branch, Employee


class BaseTestCase(APITestCase):
	def setUp(self):
		fake = Faker()

		self.customer = Customer.objects.create(
			name='John Doe',
			uid='1234567890',
			email='john.doe@example.com',
			phone='123-456-7890',
			address='123 Main St'
		)
		self.branch = Branch.objects.create(
			name='Main',
			address='123 Main St',
		)
		self.username = 'testuser'
		self.password = 'testpassword'

		self.user = User.objects.create_user(self.username, password=self.password)

		self.employee = Employee.objects.create(
			name='John Doe',
			uid='1234567890',
			email="john@stylist.com",
			phone='123-456-7890',
			branch=self.branch,
			user=self.user
		)

		self.dog = Dog.objects.create(
			name='Fido',
			breed='Golden Retriever',
			owner=self.customer
		)
		self.product = Product.objects.create(
			name='Shampoo',
			cost=Decimal('5.00')
		)
		self.service = Service.objects.create(
			name='Bathing',
			cost=Decimal('25.00'),
			duration=fake.time_delta()
		)
		self.url = reverse('appointment_employee_create_api_view')  # Replace with the actual URL name

		self.client.force_authenticate(user=self.user)

	def tearDown(self) -> None:
		self.client.logout()