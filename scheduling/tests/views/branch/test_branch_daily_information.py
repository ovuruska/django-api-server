import datetime

from common.auth_test_case import EmployeeAuthTestCase
from scheduling.models import Branch, Customer, Dog, Appointment, Employee, EmployeeWorkingHour


class TestBranchDailyInformationAPIView(EmployeeAuthTestCase):

	def setUp(self):
		super().setUp()
		self.branch = Branch.objects.create(name='Main Branch', address='123 Main St')

		self.customer = Customer.objects.create(name='John Doe')
		self.dog = Dog.objects.create(name='Fido', owner=self.customer)


	def test_branch_daily_information_empty(self):



		response = self.client.get(f'/api/branch/{self.branch.id}/daily?date=2025-12-28', **self.employee_headers)
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertEqual(data['employees'], [])
		self.assertEqual(data['appointments'],[])

	def test_branch_daily_information_non_empty(self):

		Employee.objects.create(name='Jane Doe', branch=self.branch)
		Appointment.objects.create(
			branch=self.branch,
			customer=self.customer,
			employee=self.employee,
			dog=self.dog,
			start=datetime.datetime(2025, 12, 28, 9, 0, 0),
			end=datetime.datetime(2025, 12, 28, 9, 30, 0),
		)
		date = datetime.datetime(2025, 12, 28, 9, 0, 0)

		EmployeeWorkingHour.objects.create(
			employee=self.employee,
			branch=self.branch,
			week_day=date.weekday(),
			start=datetime.datetime(2025, 12, 28, 9, 0, 0),
			end=datetime.datetime(2025, 12, 28, 16, 00, 0),
		)
		response = self.client.get(f'/api/branch/{self.branch.id}/daily?date=2025-12-28', **self.employee_headers)
		self.assertEqual(response.status_code, 200)
		data = response.json()

		self.assertEqual(len(data['employees']),1)
		self.assertEqual(len(data['appointments']),1 )
