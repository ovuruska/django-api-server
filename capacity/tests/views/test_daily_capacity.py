from django.apps import apps
from django.urls import reverse

from common.auth_test_case import EmployeeAuthTestCase


class GetDailyCapacityTestCase(EmployeeAuthTestCase):
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
		working_hour = EmployeeWorkingHour(start='08:00:00', end='19:00:00', week_day=1, employee=employee,
		                                   branch=branch)
		working_hour.save()
		working_hour = EmployeeWorkingHour(start='08:00:00', end='19:00:00', week_day=2, employee=employee,
		                                   branch=branch)
		working_hour.save()
		working_hour = EmployeeWorkingHour(start='08:00:00', end='19:00:00', week_day=3, employee=employee,
		                                   branch=branch)
		working_hour.save()
		working_hour = EmployeeWorkingHour(start='08:00:00', end='19:00:00', week_day=4, employee=employee,
		                                   branch=branch)
		working_hour.save()
		working_hour = EmployeeWorkingHour(start='08:00:00', end='19:00:00', week_day=5, employee=employee,
		                                   branch=branch)
		working_hour.save()

		Appointment.objects.create(start='2019-01-01 08:00:00', end='2019-01-01 09:00:00', employee=employee,
		                           branch=branch, customer=customer, dog=dog)
		Appointment.objects.create(start='2019-01-01 09:00:00', end='2019-01-01 10:00:00', employee=employee,
		                           branch=branch, customer=customer, dog=dog)
		Appointment.objects.create(start='2019-01-01 10:00:00', end='2019-01-01 13:00:00', employee=employee,
		                           branch=branch, customer=customer, dog=dog)
		Appointment.objects.create(start='2019-01-01 13:00:00', end='2019-01-01 16:00:00', employee=employee,
		                           branch=branch, customer=customer, dog=dog)
		Appointment.objects.create(start='2019-01-01 16:00:00', end='2019-01-01 17:00:00', employee=employee,
		                           branch=branch, customer=customer, dog=dog)

		Appointment.objects.create(start='2019-01-02 08:00:00', end='2019-01-02 09:00:00', employee=employee,
		                           branch=branch, customer=customer, dog=dog)
		Appointment.objects.create(start='2019-01-02 09:00:00', end='2019-01-02 10:00:00', employee=employee,
		                           branch=branch, customer=customer, dog=dog)
		Appointment.objects.create(start='2019-01-02 14:00:00', end='2019-01-02 15:00:00', employee=employee,
		                           branch=branch, customer=customer, dog=dog)

		Appointment.objects.create(start='2019-01-03 09:00:00', end='2019-01-03 11:00:00', employee=employee,
		                           branch=branch, customer=customer, dog=dog)
		Appointment.objects.create(start='2019-01-03 11:00:00', end='2019-01-03 12:00:00', employee=employee,
		                           branch=branch, customer=customer, dog=dog)

		Appointment.objects.create(start='2019-01-04 12:00:00', end='2019-01-04 14:00:00', employee=employee,
		                           branch=branch, customer=customer, dog=dog)
		Appointment.objects.create(start='2019-01-04 14:00:00', end='2019-01-04 15:00:00', employee=employee,
		                           branch=branch, customer=customer, dog=dog)
		Appointment.objects.create(start='2019-01-04 14:00:00', end='2019-01-04 16:00:00', employee=employee,
		                           branch=branch, customer=customer, dog=dog)

	def test_daily_working_hours(self):
		"""
		Day 1 is full, data should not include any day 1 slot.
		"""

		data = {'employees': [1], 'date': '2019-01-01', 'branches': [1], 'service': 'Full Grooming'}

		response = self.client.post(self.url, data=data, **self.employee_headers)
		self.assertEqual(response.status_code, 200)

		data = response.json()
		for day in data:
			self.assertNotEqual(day['date'], '2019-01-01')
		self.assertEqual(len(data),40)


	def test_daily_working_hours_2(self):
		"""
		Day 2 is full, data should not include any day 2 slot.
		"""

		data = {'employees': [1], 'date': '2019-01-02', 'branches': [1], 'service': 'Full Grooming'}

		response = self.client.post(self.url, data=data, **self.employee_headers)
		self.assertEqual(response.status_code, 200)

		data = response.json()
		self.assertEqual(len(data),40)
