from django.contrib.auth.models import User
# Path: authorization/tests/views/test_customer_login.py
from django.test import TestCase
from django.urls import reverse
from django.apps import apps

Customer = apps.get_model("scheduling", "Customer")

class TestCustomerLogin(TestCase):
	email = "a@a.com"
	password=  "123456"
	url = reverse("authorization/customer-login")

	def setUp(self) -> None:
		#Create a user
		self.user = User.objects.create_user(username=self.email,password=self.password)
		self.customer = Customer.objects.create(user=self.user,name="Test Customer")

	def tearDown(self) -> None:
		self.user.delete()
		self.customer.delete()


	def test_customer_login(self):
		# Test that a customer can login
		body = {"email": self.email, "password": self.password}
		response = self.client.post(self.url,body,format="json")
		self.assertEqual(response.status_code, 200)

	def test_customer_fail_login(self):
		body = {"email": self.email, "password": "wrong password"}
		response = self.client.post(self.url,body,format="json")
		self.assertEqual(response.status_code, 400)

	def test_missing_email(self):
		body = {"password": self.password}
		response = self.client.post(self.url,body,format="json")
		self.assertEqual(response.status_code, 400)

	def test_missing_password(self):
		body = {"email": self.email}
		response = self.client.post(self.url,body,format="json")
		self.assertEqual(response.status_code, 400)


