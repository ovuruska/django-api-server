from dateutil.relativedelta import relativedelta
from django.apps import apps
from django.db.models import Q

from capacity.selectors.common import CapacityCalculationParams
from capacity.selectors.utils import get_work_intervals, get_tasks, get_capacity_between_interval

Branch = apps.get_model('scheduling', 'Branch')


class CapacityResult:
	def __init__(self, branch, date, morning_capacity, afternoon_capacity):
		self.branch = branch
		self.date = date
		self.morning_capacity = morning_capacity
		self.afternoon_capacity = afternoon_capacity

	def __hash__(self):
		return hash((self.branch, self.date))

	def __dict__(self):
		return {
			'branch': self.branch,
			'date': self.date,
			'morning_capacity': self.morning_capacity,
			'afternoon_capacity': self.afternoon_capacity
		}

def get_daily_capacity_list(date, branches,N = 40):

	return_value = []
	EmployeeWorkingHour = apps.get_model('scheduling', 'EmployeeWorkingHour')
	Appointment = apps.get_model('scheduling', 'Appointment')
	working_hours = EmployeeWorkingHour.objects.filter(
		Q(branch_id__in=branches))

	# Use lambda functions to cache in a function context. This is a hacky way to do it, but it works.

	if working_hours is []:
		return return_value
	start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
	end_date = start_date + relativedelta(days=1)

	branch_cache = {    }

	while len(return_value) < N and start_date< date + relativedelta(years=1):

		for branch in branches:
			employees = working_hours.filter(branch_id=branch).values_list('employee_id', flat=True).distinct()

			appointments = Appointment.objects.filter(start__gt=start_date, start__lt=end_date,branch_id=branch,
			                                          employee__in=employees)

			work_intervals = get_work_intervals(working_hours.filter(branch_id=branch),date)
			tasks = get_tasks(appointments)
			params = CapacityCalculationParams(start_date, end_date, work_intervals, tasks)

			result = get_capacity_between_interval(params)[0]
			if result['morning_capacity'] < 0.8 and result['afternoon_capacity'] < 0.8:
				result['date'] = start_date.date()
				"""
				{
					'branch': {
						'id': 1,   
						'name': 'branch1'
						}
				"""
				branch_cache[branch] = branch_cache.get(branch, Branch.objects.get(id=branch))
				branch_entity = branch_cache[branch]
				result['branch'] = {
					'id': branch_entity.id,
					'name': branch_entity.name
				}
				return_value.append(result)
		start_date += relativedelta(days=1)
		end_date += relativedelta(days=1)
	return return_value[:N]
