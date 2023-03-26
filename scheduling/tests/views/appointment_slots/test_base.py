import datetime

from django.urls import reverse

from common.auth_test_case import CustomerAuthTestCase
from common.roles import Roles
from scheduling.models import Branch, Employee, EmployeeWorkingHour
from scheduling.tests.views.appointment_slots.scenario import ScenarioTestCase


class AppointmentSlotTestBaseCase(ScenarioTestCase):

	url = reverse("employee_free_times")

	def test_full_grooming(self):
		payload = {
			"employees":[],
			"branches":[],
			"duration":60,
			"service_type":"Full Grooming",
			"date":self.get_now()
		}
		response = self.client.post(self.url, **self.customer_headers, data=payload, format='json')
		self.assertEqual(response.status_code, 200)
		#
		self.assertEqual(len(response.data), 40)
		data = response.data
		# check if the data is sorted
		self.assertEqual(sorted(data, key=lambda x: x['start']), data)

	def test_we_wash(self):
		payload = {
			"employees":[],
			"branches":[],
			"duration":60,
			"service_type":"Full Grooming",
			"date":self.get_now()
		}
		response = self.client.post(self.url, **self.customer_headers, data=payload, format='json')
		self.assertEqual(response.status_code, 200)
		#
		self.assertEqual(len(response.data), 40)
		# check if the data is sorted
		data =  response.data
		self.assertEqual(sorted(data, key=lambda x: x['start']), data)