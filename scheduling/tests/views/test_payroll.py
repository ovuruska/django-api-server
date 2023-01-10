import datetime

from scheduling.common import Mock
from django.test import TestCase

from scheduling.models import Employee, Appointment


class PayrollTestCase(TestCase):
	def setUp(self):
		self.mock = Mock()
		self.data = self.mock.generate()

	def tearDown(self):
		self.mock.remove(self.data)


	def test_get_all(self):
		branch_id = 1
		response = self.client.get(f"/api/payrolls?branch={branch_id}")
		self.assertEqual(response.status_code, 200)
		data = response.data
		employees = Appointment.objects.filter(branch__id=1).values("employee__name").order_by("employee__name").distinct()
		self.assertEqual(len(data), len(employees))


	def test_get_all_by_name(self):
		branch_name = self.data["branches"][0].name
		response = self.client.get(f"/api/payrolls?branch__name={branch_name}")
		self.assertEqual(response.status_code, 200)
		data = response.data
		employees = Appointment.objects.filter(branch__name=branch_name).values("employee__name").order_by("employee__name").distinct()
		self.assertEqual(len(data), len(employees))