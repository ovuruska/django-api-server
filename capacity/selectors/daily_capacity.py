from dateutil.relativedelta import relativedelta
from django.apps import apps
from django.db.models import Q

from capacity.selectors.common import CapacityCalculationParams
from capacity.selectors.utils import get_work_intervals, get_tasks, get_capacity_between_interval


def get_daily_capacity_list(date, branches,N = 40):

	return_value = []
	EmployeeWorkingHour = apps.get_model('scheduling', 'EmployeeWorkingHour')
	Appointment = apps.get_model('scheduling', 'Appointment')
	working_hours = EmployeeWorkingHour.objects.filter(
		Q(branch_id__in=branches))

	# Use lambda functions to cache in a function context. This is a hacky way to do it, but it works.

	if working_hours is None:
		return return_value

	while len(return_value) < N:
		start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
		end_date = start_date + relativedelta(days=1)
		for branch in branches:
			employees = EmployeeWorkingHour.objects.filter(branch_id=branch).values_list('employee_id', flat=True)

			appointments = Appointment.objects.filter(start__gt=start_date, start__lt=end_date,
			                                          employee__in=employees)

			work_intervals = get_work_intervals(working_hours.filter(branch_id=branch),date)
			tasks = get_tasks(appointments)
			params = CapacityCalculationParams(date, end_date, work_intervals, tasks)

			results = get_capacity_between_interval(params)
			results = [{
				'branch': branch,
				**result
			}for result in results if result['morning_capacity'] < 0.8 and result['afternoon_capacity'] < 0.8]

			return_value.extend(results)
		date += relativedelta(days=1)
	return return_value[:N]
