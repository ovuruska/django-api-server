import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from knox.models import AuthToken

from common.auth_test_case import EmployeeAuthTestCase
from common.roles import Roles
from scheduling.models import Employee, Branch, EmployeeWorkingHour


class TestBranchEmployeesAPIView(EmployeeAuthTestCase):


	def setUp(self):
		super().setUp()
		self.branch = Branch.objects.create(name='Main Branch', address='123 Main St')
		self.branch.save()

		self.employee = Employee.objects.create(name='Jane Doe', branch=self.branch)
		date = datetime.datetime(2025, 12, 28, 9, 0, 0)

		EmployeeWorkingHour.objects.create(
			employee=self.employee,
			branch=self.branch,
			week_day=date.weekday(),
			start=datetime.datetime(2025, 12, 28, 9, 0, 0),
			end=datetime.datetime(2025, 12, 28, 16, 00, 0),
		)

	def test_branch_employees_view(self):
		response = self.client.get(f'/api/branch/{self.branch.id}/employees?date=2025-12-28', **self.employee_headers)
		self.assertEqual(response.status_code, 200)

	def test_branch_employees_view(self):
		response = self.client.get(f'/api/branch/{self.branch.id}/employees?date=2025-12-28', **self.employee_headers)
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertEqual(len(data), 1)
		self.assertEqual(data[0]['name'], 'Jane Doe')