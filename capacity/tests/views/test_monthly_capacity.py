import datetime

from django.apps import apps

from common.auth_test_case import EmployeeAuthTestCase


class GetMonthlyCapacityTestCase(EmployeeAuthTestCase):

	delta = 0.1

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

	def test_get_monthly_capacity(self):
		data = {
			'date': '01/2019',
			'branches': [1],
			'employees': [2],
			'service': 'We Wash'
		}
		response = self.client.post('/api/capacity/monthly', data=data, content_type='application/json',
		                            **self.employee_headers)
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertEqual(len(data),31)
		# Day 1
		self.assertEqual(data[0]['date'], '2019-01-01')
		self.assertAlmostEqual(data[0]['morning_capacity'], 0.45,delta=self.delta)
		self.assertAlmostEqual(data[0]['afternoon_capacity'], 0.63,delta=self.delta)

		# Day 2
		self.assertEqual(data[1]['date'], '2019-01-02')
		self.assertAlmostEqual(data[1]['morning_capacity'], 0.4, delta=self.delta)
		self.assertAlmostEqual(data[1]['afternoon_capacity'], 0.25, delta=self.delta)

		# Day 3
		self.assertEqual(data[2]['date'], '2019-01-03')
		self.assertAlmostEqual(data[2]['morning_capacity'], 0.7, delta=self.delta)
		self.assertAlmostEqual(data[2]['afternoon_capacity'], 0.0, delta=self.delta)

		# Day 4
		self.assertEqual(data[3]['date'], '2019-01-04')
		self.assertAlmostEqual(data[3]['morning_capacity'], 0.4, delta=self.delta)
		self.assertAlmostEqual(data[3]['afternoon_capacity'], 0.6, delta=self.delta)



		for day in data[4:]:

			date_of_day = datetime.datetime.strptime(day['date'], '%Y-%m-%d').date()
			# No slots in weekend :)
			if date_of_day.weekday() == 6 or date_of_day.weekday() == 0:
				self.assertAlmostEqual(day['morning_capacity'], 1,delta=self.delta)
				self.assertAlmostEqual(day['afternoon_capacity'],1,delta=self.delta)
			else:

				self.assertAlmostEqual(day['morning_capacity'], 0,delta=self.delta)
				self.assertAlmostEqual(day['afternoon_capacity'],0,delta=self.delta)


	def test_get_monthly_capacity_no_available_full_groomer(self):
		data = {
			'date': '01/2019',
			'branches': [1],
			'employees': [1],
			'service': 'Full Grooming'
		}
		response = self.client.post('/api/capacity/monthly', data=data, content_type='application/json',
		                            **self.employee_headers)
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertEqual(len(data),31)

		for day in data:
			self.assertEqual(day['morning_capacity'], 1)
			self.assertEqual(day['afternoon_capacity'], 1)

	def test_get_monthly_capacity_2(self):
		data = {
			'date': '01/2019',
			'branches': [1],
			'employees': [2],
			'service': 'We Wash'
		}
		response = self.client.post('/api/capacity/monthly', data=data, content_type='application/json',
		                            **self.employee_headers)
		self.assertEqual(response.status_code, 200)
		data = response.json()

		self.assertEqual(len(data),31)
		self.assertAlmostEqual(data[0]['morning_capacity'], 0.45,delta=self.delta)
		self.assertAlmostEqual(data[0]['afternoon_capacity'], 0.63,delta=self.delta)

	def test_get_monthly_capacity_get_employees_in_branch(self):
		data = {
			'date': '01/2019',
			'branches': [1],
			'employees': [],
			'service': 'We Wash'
		}
		response = self.client.post('/api/capacity/monthly', data=data, content_type='application/json',
		                            **self.employee_headers)
		self.assertEqual(response.status_code, 200)
		data = response.json()

		self.assertEqual(len(data),31)
		self.assertAlmostEqual(data[0]['morning_capacity'], 0.45,delta=self.delta)
		self.assertAlmostEqual(data[0]['afternoon_capacity'], 0.63,delta=self.delta)

	def test_get_monthly_capacity_get_employees_in_branch_2(self):
		data = {
			'date': '01/2019',
			'branches': [1],
			'employees': [1],
			'service': 'We Wash'
		}
		response = self.client.post('/api/capacity/monthly', data=data, content_type='application/json',
		                            **self.employee_headers)
		self.assertEqual(response.status_code, 200)
		data = response.json()

		self.assertEqual(len(data), 31)
		self.assertAlmostEqual(data[0]['morning_capacity'], 0.45, delta=self.delta)
		self.assertAlmostEqual(data[0]['afternoon_capacity'], 0.63, delta=self.delta)
