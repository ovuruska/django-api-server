from django.urls import reverse

from common.auth_test_case import EmployeeAuthTestCase


class GetDailyCapacity400TestCase(EmployeeAuthTestCase):

	url = reverse("capacity/get_daily_capacity")

	def test_with_invalid_service(self):

		data = {
			"date": "2023-04-01",
			"service": "service",
		}

		response = self.client.post(self.url, data=data,**self.employee_headers)
		self.assertEqual(response.status_code, 400)

	def test_with_invalid_date(self):

		data = {
			"date": "2023/12",
			"service": "We Wash",
		}

		response = self.client.post(self.url, data=data,**self.employee_headers)
		self.assertEqual(response.status_code, 400)

	def test_with_invalid_date_2(self):

		data = {
			"date": "2023-12",
			"service": "We Wash",
		}
		response = self.client.post(self.url, data=data,**self.employee_headers)
		self.assertEqual(response.status_code, 400)

	def test_with_invalid_date_3(self):

		data = {
			"date": "2023-12-01-12",
			"service": "We Wash",
		}
		response = self.client.post(self.url, data=data,**self.employee_headers)
		self.assertEqual(response.status_code, 400)

