import datetime
import time

from scheduling.common import Mock

from django.test import TestCase

class AppointmentRetrievalBenchmarkTest10000(TestCase):

	root_url = "/api/schedule/appointments"
	number_of_appointments = 10000

	def setUp(self) :
		self.mock = Mock(number_of_appointments=self.number_of_appointments)
		self.data = self.mock.generate()

	def tearDown(self) -> None:
		self.mock.remove(self.data)


	def test_get_dashboard(self):
		branch_id = self.data["branches"][0].id
		current_date = datetime.datetime.now()
		start_gt = current_date.strftime("%Y-%m-%d")
		end_lt = (current_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
		request_start = time.time()
		response = self.client.get(self.root_url+"?branch="+str(branch_id)+"&start__gt="+str(start_gt)+"&start__lt="+str(end_lt))

		length = len(response.data)
		request_end = time.time()
		print("Request took: "+str(request_end-request_start)+" seconds. It returned "+str(length)+" appointments.")

		self.assertEqual(response.status_code, 200)

		for appointment in response.data:
			self.assertEqual(appointment["branch"]["id"], branch_id)
			self.assertGreaterEqual(appointment["start"], start_gt)
			self.assertLessEqual(appointment["start"], end_lt)
		self.assertLess(request_end-request_start, 0.5)
