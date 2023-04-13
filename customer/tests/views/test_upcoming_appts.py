from django.urls import reverse
from common.auth_test_case import CustomerAuthTestCase
from customer.tests.views.generate_customer_appts import generate_upcoming_appts


class TestUpcomingAppts(CustomerAuthTestCase):
	url = reverse("customer/appointments/upcoming")

	def setUp(self):
		super().setUp()



	def test_upcoming_appts_unauthorized(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 401)

	def test_upcoming_appts(self):
		response = self.client.get(self.url,**self.customer_headers)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data, {
			"count": 0,
			"next": None,
			"previous": None,
			"results": []
		})

	def test_upcoming_appts_available(self):
		generate_upcoming_appts(self.customer, 5)
		response = self.client.get(self.url,**self.customer_headers)
		self.assertEqual(response.status_code, 200)
		response_data = response.json()
		results = response_data["results"]
		self.assertEqual(len(results), 0)
		self.assertEqual(response_data["count"], 5)

	def test_with_limit_offset(self):
		generate_upcoming_appts(self.customer, 5)
		response = self.client.get(self.url, {"limit":1}, **self.customer_headers)
		self.assertEqual(response.status_code, 200)
		response_data = response.json()
		results = response_data["results"]
		self.assertEqual(len(results),1 )
		self.assertEqual(response_data["count"], 5)


	def test_with_limit_offset_2(self):
		generate_upcoming_appts(self.customer, 5)
		response = self.client.get(self.url, {"limit":2}, **self.customer_headers)
		self.assertEqual(response.status_code, 200)
		response_data = response.json()
		results = response_data["results"]
		self.assertEqual(len(results),2 )


	def test_with_limit_offset_3(self):
		generate_upcoming_appts(self.customer, 5)
		response = self.client.get(self.url, {"limit":2, "offset":2}, **self.customer_headers)
		self.assertEqual(response.status_code, 200)
		response_data = response.json()
		results = response_data["results"]
		self.assertEqual(len(results),2 )
		self.assertEqual(response_data["count"], 5)

	def test_with_limit_offset_empty(self):

		response = self.client.get(self.url, {"limit":2, "offset":16}, **self.customer_headers)
		self.assertEqual(response.status_code, 200)
		response_data = response.json()
		results = response_data["results"]
		self.assertEqual(len(results),0 )
		self.assertEqual(response_data["count"], 0)

	def test_with_limit_offset_empty_2(self):

		response = self.client.get(self.url, {"limit":0}, **self.customer_headers)
		self.assertEqual(response.status_code, 200)
		response_data = response.json()
		results = response_data["results"]
		self.assertEqual(len(results),0 )
		self.assertEqual(response_data["count"], 0)