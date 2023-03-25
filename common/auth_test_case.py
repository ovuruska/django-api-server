from django.contrib.auth.models import User
from django.test import TestCase
from knox.models import AuthToken

from common.roles import Roles
from scheduling.models import Employee, Customer


class EmployeeAuthTestCase(TestCase):

	def setUp(self):
		self.employee_username = 'testemployee'
		self.employee_password = 'testpassword'
		self.employee = Employee.objects.create(name='John Doe', email='john@example.com',
		                                        role=Roles.EMPLOYEE_FULL_GROOMING)
		self.user = User.objects.create_user(
			username=self.employee_username,
			password=self.employee_password
		)
		self.employee.user = self.user
		self.employee.save()
		# Login
		token_instance, token = AuthToken.objects.create(self.user)
		self.employee_headers = {'HTTP_AUTHORIZATION': f'Token {token}'}


class CustomerAuthTestCase(TestCase):

	def setUp(self):
		self.customer_username = 'testcustomer'
		self.customer_password = 'testpassword'
		self.customer = Customer.objects.create(name='John Doe', email='john@example.com',
		                                        role=Roles.EMPLOYEE_FULL_GROOMING)
		self.user = User.objects.create_user(
			username=self.customer_username,
			password=self.customer_password
		)
		self.customer.user = self.user
		self.customer.save()
		# Login
		token_instance, token = AuthToken.objects.create(self.user)
		self.customer_headers = {'HTTP_AUTHORIZATION': f'Token {token}'}
