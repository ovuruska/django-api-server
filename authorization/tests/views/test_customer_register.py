
from django.test import TestCase
from django.urls import reverse

class TestCustomerRegisterAPIView(TestCase):
	url = reverse("authorization/customer-register")


	def test_customer_register_api_view(self):
		data = {
			"email": "test@tenet.com",
			"password": "test1234",
			"first_name": "test",
			"last_name": "lastname"
		}

		response = self.client.post(self.url, data=data, format="json")
		self.assertEqual(response.status_code, 200)
		response_json = response.json()
		self.assertEqual(response_json.get("user").get("username"), data.get("email"))
		self.assertEqual(response_json.get("profile").get("name"), f"{data.get('first_name')} {data.get('last_name')}")
		self.assertEqual(response_json.get("profile").get("user"), 1)
		self.assertEqual(response_json.get("profile").get("role"), 1)
		self.assertEqual(response_json.get("profile").get("validated"), True)
		self.assertEqual(response_json.get("profile").get("id"), 1)
		self.assertEqual(response_json.get("profile").get("uid"), "")
		self.assertEqual(response_json.get("profile").get("email"), "test@tenet.com")
		self.assertEqual(response_json.get("profile").get("phone"), "")
		self.assertEqual(response_json.get("profile").get("address"), "")

	def test_customer_register_api_view_invalid_email(self):
		data = {
			"email": "test@tenet",
			"password": "test1234",
			"first_name": "test",
			"last_name": "lastname"
		}

		response = self.client.post(self.url, data=data, format="json")
		self.assertEqual(response.status_code, 400)


	def test_customer_register_api_view_invalid_missing_field(self):
		data = {
	"first_name": "test",
			"last_name": "lastname"
		}
		response = self.client.post(self.url, data=data, format="json")
		self.assertEqual(response.status_code, 400)

	def test_correct_account_with_token(self):
		token = "2c0d19194c042d7fe976fb9240915007a402b3d8228a1958b59b54daf816fb84"
		headers = {'HTTP_AUTHORIZATION': f'Token {token}'}
		data = {
			"email": "new@tenet.com",
			"password": "test1234",
			"first_name": "test",
			"last_name": "lastname"
		}
		response = self.client.post(self.url,data=data,format="json",**headers)
		self.assertEqual(response.status_code, 200)