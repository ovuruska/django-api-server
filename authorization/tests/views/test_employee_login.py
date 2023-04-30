from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.apps import apps

class EmployeeLoginTestCase(TestCase):
	email = "a@a.com"
	password = "123456"
	url = reverse("authorization/employee-login")

	def setUp(self) -> None:
		# Create a user
		self.user = User.objects.create_user(username=self.email, password=self.password)
		# Create a customer
		self.employee = apps.get_model("scheduling", "Employee").objects.create(user=self.user, name="Test Employee")

	def tearDown(self) -> None:
		self.user.delete()
		self.employee.delete()

	def test_employee_login(self):
		# Test that a customer can login
		body = {"username": self.email, "password": self.password}
		response = self.client.post(self.url, body, format="json")
		self.assertEqual(response.status_code, 200)

	def test_employee_fail_to_login(self):
		body = {"username": self.email, "password": "wrong password"}
		response = self.client.post(self.url, body, format="json")
		self.assertEqual(response.status_code, 400)

	def test_missing_username(self):
		body = {"password": self.password}
		response = self.client.post(self.url, body, format="json")
		self.assertEqual(response.status_code, 400)

	def test_missing_password(self):
		body = {"username": self.email}
		response = self.client.post(self.url, body, format="json")
		self.assertEqual(response.status_code, 400)

	def test_correct_account_with_token(self):
		body = {"username": self.email, "password": self.password}
		token = "2c0d19194c042d7fe976fb9240915007a402b3d8228a1958b59b54daf816fb84"
		headers = {'HTTP_AUTHORIZATION': f'Token {token}'}
		response = self.client.post(self.url, body, format="json",**headers)
		self.assertEqual(response.status_code, 200)

