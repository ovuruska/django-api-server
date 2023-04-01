from datetime import datetime

import pytz
from django.apps import apps
from django.test import TestCase

from capacity.selectors.monthly_capacity import get_tasks, CapacityTask


Appointment = apps.get_model('scheduling', 'Appointment')


class GetTasksTestCase(TestCase):

	def setUp(self):
		Appointment = apps.get_model('scheduling', 'Appointment')
		Branch = apps.get_model('scheduling', 'Branch')
		Employee = apps.get_model('scheduling', 'Employee')
		Customer = apps.get_model('scheduling', 'Customer')
		Dog = apps.get_model('scheduling', 'Dog')

		customer = Customer.objects.create()
		dog = Dog.objects.create(owner=customer)

		branch = Branch.objects.create()
		employee = Employee.objects.create(branch=branch)
		Appointment.objects.create(start='2019-01-01 00:00:00', end='2019-01-01 00:00:00', employee=employee,branch=branch,customer=customer,dog=dog)

	def test_get_tasks(self):
		appointments = Appointment.objects.all()
		self.assertEqual(len(appointments), 1)
		tasks = get_tasks(appointments)
		self.assertEqual(len(tasks), 1)
		self.assertEqual(tasks[0].start.replace(tzinfo=pytz.UTC), datetime(2019, 1, 1, 0, 0, tzinfo=pytz.UTC))
		self.assertEqual(tasks[0].end.replace(tzinfo=pytz.UTC), datetime(2019, 1, 1, 0, 0, tzinfo=pytz.UTC))
		self.assertEqual(tasks[0].worker, 1)
		self.assertEqual(type(tasks[0]), CapacityTask)