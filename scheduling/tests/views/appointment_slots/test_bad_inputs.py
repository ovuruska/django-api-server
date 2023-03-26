import datetime

from django.urls import reverse

from common.auth_test_case import CustomerAuthTestCase
from common.roles import Roles
from scheduling.models import Branch, Employee


class AppointmentSlotTestBadInputsCase(CustomerAuthTestCase):

	url = reverse("employee_free_times")


	def setUp(self):
		super().setUp()

		self.branch_1 = Branch.objects.create(
			name='Branch 1',
			address='Test Address',
			phone='123456789',
		)
		self.branch_2 = Branch.objects.create(
			name='Branch 2',
			address='Test Address',
			phone='123456789',
		)

		self.employee_1 = Employee.objects.create(
			name='Employee 1',
			branch=self.branch_1,
			role=Roles.EMPLOYEE_FULL_GROOMING,
		)

		self.employee_2 = Employee.objects.create(
			name='Employee 2',
			branch=self.branch_2,
			role=Roles.EMPLOYEE_FULL_GROOMING,
		)

		self.employee_3 = Employee.objects.create(
			name='Employee 3',
			branch=self.branch_1,
			role=Roles.EMPLOYEE_WE_WASH,
		)

		self.employee_4 = Employee.objects.create(
			name='Employee 4',
			branch=self.branch_2,
			role=Roles.EMPLOYEE_WE_WASH,
		)

		self.url = reverse("employee_free_times")

	@staticmethod
	def get_now() -> str:

		now = datetime.datetime.now().replace(microsecond=0,second=0)
		formatted_time = now.strftime("%Y-%m-%d")
		return formatted_time

	@staticmethod
	def format_time(time:datetime.datetime) -> str:
		# 2023-02-01T00:00:00
		formatted_time = time.strftime("%Y-%m-%d")
		return formatted_time

	def test_infinite_loop(self):

		payload = {
			"employees":[],
			"branches":[],
			"duration":60,
			"service_type":"We Wash",
			"date":self.get_now()
		}
		response = self.client.post(self.url, **self.customer_headers, data=payload, format='json')
		self.assertEqual(response.status_code, 200)
		#
		self.assertEqual(len(response.data), 0)

	def test_infinite_loop_2(self):

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
		self.assertEqual(len(response.data), 0)


	def test_previous_time(self):

		# Now or newer :)

		payload = {
			"employees":[],
			"branches":[],
			"duration":60,
			"service_type":"Full Grooming",
			"date":self.format_time(datetime.datetime(1,0, 0, 0, 0, 0, 0))
		}
		response = self.client.post(self.url, **self.customer_headers, data=payload, format='json')
		self.assertEqual(response.status_code, 400)
