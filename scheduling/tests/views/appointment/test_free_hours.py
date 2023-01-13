from datetime import datetime, timedelta

from django.test import TestCase

from scheduling.models import Branch, Employee, Customer, Dog, Appointment
from scheduling.tests.views.mock import branches, employees, customers, dogs
from scheduling.common.mock import Mock

class FreeHoursTestCase(TestCase):
	"""

	"""

	test_url = "/appointment/1"

	def setUp(self):
		self.mock = Mock()
		self.data = self.mock.generate()

	def tearDown(self):
		self.mock.remove(self.data)

	def test_free_hours(self):

		results = self.client.get("/api/branch/1/free_hours?date=2020-01-01")
		self.assertEqual(results.status_code, 200)
