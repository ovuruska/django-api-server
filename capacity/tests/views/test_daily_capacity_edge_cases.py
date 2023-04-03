from django.apps import apps
from django.urls import reverse

from common.auth_test_case import EmployeeAuthTestCase


class GetDailyCapacityEdgeCasesTestCase(EmployeeAuthTestCase):

	url = reverse("capacity/get_daily_capacity")

	def setUp(self) -> None:
		super().setUp()
		Employee = apps.get_model('scheduling', 'Employee')
		Branch = apps.get_model('scheduling', 'Branch')
		Appointment = apps.get_model('scheduling', 'Appointment')
		Customer = apps.get_model('scheduling', 'Customer')
		Dog = apps.get_model('scheduling', 'Dog')
		EmployeeWorkingHour = apps.get_model('scheduling', 'EmployeeWorkingHour')

		branch = Branch.objects.create()
		employee = Employee.objects.create(branch=branch)
		customer = Customer.objects.create()
		dog = Dog.objects.create(owner=customer)




	def test_get_daily_capacity_infinity_loop_test_1(self):
		data = {
			'date': '2019-01-01',
			'service': 'We Wash',
		}
		response = self.client.post(self.url, data=data,**self.employee_headers)
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertEqual(len(data),0)

	def test_get_daily_capacity_infinity_loop_test_2(self):
		data = {
			'date': '2019-01-02',
			'service': 'Full Grooming',
		}
		response = self.client.post(self.url, data=data,**self.employee_headers)
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertEqual(len(data),0)


