from datetime import datetime

import pytz
from django.apps import apps
from django.test import TestCase

from capacity.selectors.utils import get_work_intervals
from capacity.selectors.common import WorkInterval

EmployeeWorkingHour = apps.get_model('scheduling', 'EmployeeWorkingHour')


class GetWorkIntervalsTestCase(TestCase):

	def setUp(self):
		Branch = apps.get_model('scheduling', 'Branch')
		Employee = apps.get_model('scheduling', 'Employee')

		branch = Branch.objects.create()
		employee = Employee.objects.create(branch=branch)
		working_hour = EmployeeWorkingHour(start='00:00:00', end='16:00:00', week_day=5, employee=employee,branch=branch)
		working_hour.save()

	def test_get_tasks(self):
		working_hours = EmployeeWorkingHour.objects.all()
		self.assertEqual(len(working_hours), 1)
		work_intervals = get_work_intervals(working_hours)
		self.assertEqual(len(work_intervals), 1)
		self.assertEqual(work_intervals[0].start, datetime(2019, 1, 1, 0, 0, tzinfo=pytz.UTC).time())
		self.assertEqual(work_intervals[0].end, datetime(2019, 1, 1, 16, 0, tzinfo=pytz.UTC).time())
		self.assertEqual(work_intervals[0].worker_id, 1)
		self.assertEqual(type(work_intervals[0]), WorkInterval)