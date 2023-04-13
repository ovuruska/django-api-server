from django.apps import apps
from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth.models import User
from unittest.mock import patch

Branch = apps.get_model("scheduling","Branch")
Customer = apps.get_model("scheduling","Customer")
Appointment = apps.get_model("scheduling","Appointment")
Employee = apps.get_model("scheduling","Employee")
EmployeeWorkingHour = apps.get_model("scheduling","EmployeeWorkingHour")


class AddAppointmentsCommandTestCase(TestCase):
	def setUp(self):
		self.username = 'new-customer'
		self.password = 'testpassword'
		self.email = 'new-customer@example.com'
		self.user = User.objects.create_user(username=self.username, password=self.password, email=self.email)
		self.customer = Customer.objects.create(user=self.user)
		self.branch = Branch.objects.create()
		self.employee = Employee.objects.create(user=self.user, branch=self.branch)
		for week_day in range(7):
			self.employee_working_hour = EmployeeWorkingHour.objects.create(employee=self.employee, branch=self.branch,week_day=week_day,start="0:00",end="23:00")


	def tearDown(self):
		Customer.objects.filter(user=self.user).delete()
		User.objects.filter(username=self.username).delete()
		Employee.objects.filter(user=self.user).delete()
		EmployeeWorkingHour.objects.filter().delete()
		Branch.objects.filter().delete()

	def test_add_appointments_success(self):
		num_appointments_before = Appointment.objects.filter(customer_id=self.customer).count()
		num_appointments_to_add = 5
		with patch('builtins.input', side_effect=[self.username, str(num_appointments_to_add)]):
			call_command('add_appointments')

		num_appointments_after = Appointment.objects.filter(customer_id=self.customer).count()
		self.assertEqual(num_appointments_after, num_appointments_before + num_appointments_to_add)

	def test_add_appointments_unavailable_username(self):
		unavailable_username = 'non_existent_customer'
		with patch('builtins.input', side_effect=[unavailable_username]):
			with self.assertRaises(Exception) as context:
				call_command('add_appointments')

