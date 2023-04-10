import datetime

from django.apps import apps
from django.urls import reverse

from common.auth_test_case import EmployeeAuthTestCase
from common.roles import Roles


class DailyAvailableScenarioTestCase(EmployeeAuthTestCase):
	delta = 0.1
	url = reverse('available/daily_available')

	def setUp(self) -> None:
		super().setUp()
		Employee = apps.get_model('scheduling', 'Employee')
		Branch = apps.get_model('scheduling', 'Branch')
		Appointment = apps.get_model('scheduling', 'Appointment')
		Customer = apps.get_model('scheduling', 'Customer')
		Dog = apps.get_model('scheduling', 'Dog')
		EmployeeWorkingHour = apps.get_model('scheduling', 'EmployeeWorkingHour')

		branch = Branch.objects.create()
		employee = Employee.objects.create(branch=branch,role= Roles.EMPLOYEE_WE_WASH)
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
		Appointment.objects.create(start='2019-01-01 13:00:00', end='2019-01-01 16:00:00', employee=employee,
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

	def test_daily_fully_available(self):

		durations = [
			30,60,120,240
		]
		for duration in durations:

			data = {
				"employees": [2],
				"date": "2019-01-08",
				"duration": duration,
				"service":"We Wash"
			}

			response = self.client.post(self.url, data=data,**self.employee_headers)
			self.assertEqual(response.status_code, 200)
			data = response.json()
			current_start = datetime.datetime.strptime('2019-01-08 08:00:00', '%Y-%m-%d %H:%M:%S')
			current_end = current_start + datetime.timedelta(minutes=duration)
			for slot in data:
				self.assertEqual(slot['employee']['id'],2 )
				self.assertEqual(slot['branch']['id'], 1)
				self.assertEqual(datetime.datetime.strptime(slot['start'], '%Y-%m-%dT%H:%M:%SZ'),  current_start)
				self.assertEqual(datetime.datetime.strptime(slot['end'], '%Y-%m-%dT%H:%M:%SZ'),  current_end)

				current_start += datetime.timedelta(minutes=30)
				current_end += datetime.timedelta(minutes=30)

	def test_daily_with_huge_duration(self):
		data = {
			"employees": [2],
			"date": "2019-01-08",
			"duration": 10000,
			"service":"We Wash"
		}

		response = self.client.post(self.url, data=data,**self.employee_headers)
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertEqual(len(data), 0)


	def test_daily_no_slot_full_grooming(self):
		data = {
			"employees": [2],
			"date": "2019-01-08",
			"duration": 120,
			"service":"Full Grooming"
		}

		response = self.client.post(self.url, data=data,**self.employee_headers)
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertEqual(len(data), 0)


	def test_daily_no_slot_we_wash_monday(self):
		data = {
			"employees": [2],
			"date": "2019-12-30",
			"duration": 120,
			"service":"We Wash"
		}

		response = self.client.post(self.url, data=data,**self.employee_headers)
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertEqual(len(data), 0)

	def test_daily_no_slot_we_wash_sunday(self):
		data = {
			"employees": [2],
			"date": "2019-01-06",
			"duration": 120,
			"service":"We Wash"
		}

		response = self.client.post(self.url, data=data,**self.employee_headers)
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertEqual(len(data), 0)

	def test_daily_no_slot_we_wash_with_appointments(self):
		data = {
			"employees": [2],
			"date": "2019-01-04",
			"duration": 120,
			"service":"We Wash"
		}

		response = self.client.post(self.url, data=data,**self.employee_headers)
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertEqual(len(data), 13)
