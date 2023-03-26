import datetime

from django.urls import reverse

from common.auth_test_case import CustomerAuthTestCase
from common.roles import Roles
from scheduling.models import Branch, Employee, EmployeeWorkingHour
from scheduling.tests.views.appointment_slots.scenario import ScenarioTestCase


class AppointmentSlotTestCase3(ScenarioTestCase):
	url = reverse("employee_free_times")

	def check(self,employees,item,duration,branches ):

		self.assertTrue(item['employee']['id'] in employees or item['branch']['id'] in branches)
		# start 9:00:00 => hour = 9 , minute = 0
		# end 10:00:00 => hour = 10 , minute = 0
		start = datetime.datetime.strptime(item['start'],"%Y-%m-%dT%H:%M:%S")
		end = datetime.datetime.strptime(item['end'], "%Y-%m-%dT%H:%M:%S")
		self.assertEqual((end-start).total_seconds(), duration * 60)


	def test_full_grooming(self):
		employees = [1,2]
		branches = [1,2]
		duration = 60
		payload = {
			"employees": employees,
			"branches": branches,
			"duration": duration,
			"service_type": "Full Grooming",
			"date": self.get_now()
		}
		response = self.client.post(self.url, **self.customer_headers, data=payload, format='json')
		self.assertEqual(response.status_code, 200)
		#
		self.assertEqual(len(response.data), 40)
		data = response.data
		# check if the data is sorted
		self.assertEqual(sorted(data, key=lambda x: x['start']), data)
		for item in data:
			self.check(employees,item,duration,branches)


	def test_we_wash(self):
		employees = [3,4]
		branches = [1]
		duration = 45
		payload = {
			"employees": employees,
			"branches": branches,
			"duration": duration,
			"service_type": "We Wash",
			"date": self.get_now()
		}
		response = self.client.post(self.url, **self.customer_headers, data=payload, format='json')
		self.assertEqual(response.status_code, 200)
		#
		self.assertEqual(len(response.data), 40)
		# check if the data is sorted
		data = response.data
		self.assertEqual(sorted(data, key=lambda x: x['start']), data)

		for item in data:
			self.check(employees,item,duration,branches)
