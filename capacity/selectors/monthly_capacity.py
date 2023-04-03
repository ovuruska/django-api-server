from dateutil.relativedelta import relativedelta
from django.apps import apps
from django.db.models import Q

from capacity.selectors.common import CapacityCalculationParams
from capacity.selectors.utils import get_tasks, get_work_intervals, get_capacity_between_interval
from scheduling.models import Appointment


def get_monthly_capacity(date, employees):
	EmployeeWorkingHour = apps.get_model('scheduling', 'EmployeeWorkingHour')
	first_day_of_month = date.replace(day=1)
	last_day_of_month = first_day_of_month + relativedelta(months=1, days=-1)
	working_hours = EmployeeWorkingHour.objects.filter(
		Q(employee_id__in=employees))
	appointments = Appointment.objects.filter(start__gt=first_day_of_month, start__lt=last_day_of_month,
	                                          employee__in=employees)

	work_intervals = get_work_intervals(working_hours, first_day_of_month)
	tasks = get_tasks(appointments)
	params = CapacityCalculationParams(first_day_of_month, last_day_of_month, work_intervals, tasks)

	return get_capacity_between_interval(params)


