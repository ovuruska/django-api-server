from datetime import datetime
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from scheduling.models import Customer, Product, Service, Dog

from django.utils import timezone

from django.test import TestCase
from django.contrib.auth.models import User
from faker import Faker
from knox.models import AuthToken

from common.roles import Roles
from scheduling.models import Employee, Appointment, Dog, Customer, Branch, Service, Product
from scheduling.services import create_pet_with_name
from scheduling.services.customer import create_customer_with_name


class AuthTestCase(TestCase):

	def setUp(self):
		self.username = 'testuser'
		self.employee = Employee.objects.create(name='John Doe', email='john@example.com',
		                                        role=Roles.EMPLOYEE_FULL_GROOMING)
		self.user = User.objects.create_user(username='testuser', password='testpassword')
		self.employee.user = self.user
		self.employee.save()
		# Login
		self.token_instance, self.token = AuthToken.objects.create(self.user)
		self.headers = {'HTTP_AUTHORIZATION': f'Token {self.token}'}

		fake = Faker()

		self.customer_name = 'John Doe'
		self.customer_email = 'johndoe@quicker.com'
		self.customer_phone = '1234567890'
		self.dog_name = 'Fido'
		self.dog_breed = 'Golden Retriever'
		self.branch = Branch.objects.create(name='Main Branch', address='123 Main St')
		self.employee = Employee.objects.create(user=None)  # Assuming Employee has a nullable user field
		# duration = models.DurationField()
		self.service = Service.objects.create(name='Bath', description='Dog bath service', cost=25.0,
		                                      duration=fake.time_delta())
		self.product = Product.objects.create(name='Shampoo', description='Dog shampoo', cost=10.0)


class TestAppointmentEmployeeCreateAPIView(AuthTestCase):

	def test_employee_create_appointment(self):
		# Set up the request data
		# Send a POST request to the view
		response = self.client.post('/api/schedule/appointment-employee',
		                            data={'customer_name': f"{self.customer_name}",
			                            'customer_email': f"{self.customer_email}",
			                            'customer_phone': f"{self.customer_phone}", 'dog_name': f"{self.dog_name}",
			                            'dog_breed': f"{self.dog_breed}", 'products': [self.product.id],
			                            'services': [self.service.id], "start": "2023-01-13T19:15:17",

			                            "branch_id": f"{self.branch.id}", "employee_id": f"{self.employee.id}",
			                            # Add any other required fields here
		                            }, **self.headers, format='json')

		# Check that the response is successful
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		def test_employee_create_appointment_with_nonzero_tip(self):
			# Set up the request data
			# Send a POST request to the view
			response = self.client.post('/api/schedule/appointment-employee',
			                            data={'customer_name': f"{self.customer_name}",
				                            'customer_email': f"{self.customer_email}",
				                            'customer_phone': f"{self.customer_phone}", 'dog_name': f"{self.dog_name}",
				                            'dog_breed': f"{self.dog_breed}", 'products': [self.product.id],
				                            'services': [self.service.id], "start": "2023-01-13T19:15:17", "tip": 123,
				                            "branch_id": f"{self.branch.id}", "employee_id": f"{self.employee.id}",
				                            # Add any other required fields here
			                            }, **self.headers, format='json')

			# Check that the response is successful
			self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_employee_create_appointment_with_end(self):
		# Set up the request data
		# Send a POST request to the view
		response = self.client.post('/api/schedule/appointment-employee',
		                            data={'customer_name': f"{self.customer_name}",
			                            'customer_email': f"{self.customer_email}",
			                            'customer_phone': f"{self.customer_phone}", 'dog_name': f"{self.dog_name}",
			                            'dog_breed': f"{self.dog_breed}", 'products': [self.product.id],
			                            'services': [self.service.id], "start": "2023-01-13T19:15:17",
			                            "end": "2023-01-13T19:45:17",

			                            "branch_id": f"{self.branch.id}", "employee_id": f"{self.employee.id}",
			                            # Add any other required fields here
		                            }, **self.headers, format='json')

		# Check that the response is successful
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
