import datetime

from django.urls import reverse

from common.auth_test_case import CustomerAuthTestCase
from common.roles import Roles
from scheduling.models import Branch, Employee, EmployeeWorkingHour
from scheduling.tests.views.appointment_slots.scenario import ScenarioTestCase


class AppointmentSlotTestBaseCase(ScenarioTestCase):
	url = reverse("employee_free_times")

	def check(self,employees,item,duration ):

		self.assertIn(item['employee']['id'], employees)
		start = datetime.datetime.strptime(item['start'], "%Y-%m-%dT%H:%M:%S")
		end = datetime.datetime.strptime(item['end'], "%Y-%m-%dT%H:%M:%S")
		self.assertEqual((end-start).total_seconds(), duration * 60)


	def test_full_grooming(self):
		employees = [1,2]
		duration = 60
		payload = {
			"employees": employees,
			"branches": [],
			"duration": duration,
			"service_type": "Full Grooming",
			"start_date": self.get_now()
		}
		response = self.client.post(self.url, **self.customer_headers, data=payload, format='json')
		self.assertEqual(response.status_code, 200)
		#
		self.assertEqual(len(response.data), 40)
		data = response.data
		# check if the data is sorted
		self.assertEqual(sorted(data, key=lambda x: x['start']), data)
		for item in data:
			self.check(employees,item,duration)


	def test_we_wash(self):
		employees = [3,4]
		duration = 45
		payload = {
			"employees": employees,
			"branches": [],
			"duration": duration,
			"service_type": "We Wash",
			"start_date": self.get_now()
		}
		response = self.client.post(self.url, **self.customer_headers, data=payload, format='json')
		self.assertEqual(response.status_code, 200)
		#
		self.assertEqual(len(response.data), 40)
		# check if the data is sorted
		data = response.data
		self.assertEqual(sorted(data, key=lambda x: x['start']), data)

		for item in data:
			self.check(employees,item,duration)
