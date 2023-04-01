import datetime

from django.urls import reverse

from common.auth_test_case import EmployeeAuthTestCase


class DailyAvailableViewTestCase(EmployeeAuthTestCase):
	url = reverse('available/daily_available')

	@staticmethod
	def get_next_day():
		return (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

	def test_invalid_service_name(self):
		data = {
			"employees": [1, 2],
			"branches": [1, 2],
			"service": "invalid",
			"date": self.get_next_day()
		}
		response = self.client.post(self.url,data=data, **self.employee_headers)
		self.assertEqual(response.status_code, 400)


	def test_invalid_date_wrong_format(self):
		data = {
			"employees": [1, 2],
			"branches": [1, 2],
			"service": "invalid",
			"date": "2020-01-01 12:00:00"
		}
		response = self.client.post(self.url, data=data, **self.employee_headers)
		self.assertEqual(response.status_code, 400)

	def test_invalid_date_wrong_format_v2(self):
		data = {
			"employees": [1, 2],
			"branches": [1, 2],
			"service": "invalid",
			"date": "2020/01/01"
		}
		response = self.client.post(self.url, data=data, **self.employee_headers)
		self.assertEqual(response.status_code, 400)
