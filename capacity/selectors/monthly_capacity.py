"""


"""
from datetime import datetime

from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, DAILY
from django.apps import apps
from django.db.models import Q

from scheduling.models import Appointment, EmployeeWorkingHour


class CapacityTask:
	def __init__(self, start, end, worker: int, ):
		self.start: datetime = start
		self.end: datetime = end
		self.worker: int = worker


class TaskWorker:
	def __init__(self, start, end, id: int, ):
		self.start: datetime = start
		self.end: datetime = end
		self.id: int = id


class WorkInterval:
	def __init__(self, start, end, worker_id):
		self.start: datetime = start
		self.end: datetime = end
		self.worker_id: int = worker_id


class CapacityCalculationParams:
	def __init__(self, start_date: datetime, end_date: datetime, intervals: [WorkInterval], tasks: [CapacityTask]):
		self.start_date = start_date
		self.end_date = end_date
		self.intervals = intervals
		self.tasks = tasks


def get_monthly_capacity(date, employees):
	EmployeeWorkingHour = apps.get_model('scheduling', 'EmployeeWorkingHour')
	first_day_of_month = date.replace(day=1)
	last_day_of_month = first_day_of_month + relativedelta(months=1, days=-1)
	working_hours = EmployeeWorkingHour.objects.filter(
		Q(employee_id__in=employees))
	appointments = Appointment.objects.filter(start__gt=first_day_of_month, start__lt=last_day_of_month,
	                                          employee__in=employees)

	work_intervals = get_work_intervals(working_hours,first_day_of_month)
	tasks = get_tasks(appointments)
	params = CapacityCalculationParams(first_day_of_month, last_day_of_month, work_intervals, tasks)

	return get_capacity_between_interval(params)


def get_tasks(appointments: [Appointment]) -> [CapacityTask]:
	tasks = []
	for appointment in appointments:
		# Get rid of timezone
		appointment.start = appointment.start.replace(tzinfo=None)
		appointment.end = appointment.end.replace(tzinfo=None)
		tasks.append(CapacityTask(appointment.start, appointment.end, appointment.employee.id))

	return tasks


def get_work_intervals(working_hours: [EmployeeWorkingHour],date=None) -> [WorkInterval]:
	work_intervals = []
	for working_hour in working_hours:
		if date:
			# Hacky week day fix
			week_day = working_hour.week_day
			# Get corresponding week day of date
			week_day_date = date + relativedelta(days=week_day - date.weekday())
			work_start = datetime.combine(week_day_date, working_hour.start)
			work_end = datetime.combine(week_day_date, working_hour.end)
		else:
			work_start = working_hour.start
			work_end = working_hour.end

		work_intervals.append(WorkInterval(work_start,work_end, working_hour.employee.id))

	return work_intervals


def get_total_slots(start: datetime, end: datetime, interval: int) -> int:
	if end.hour < start.hour:
		return 0
	total_slots = (end.hour - start.hour) * 60 // interval + 1
	return total_slots


def convert_time(start: datetime, end: datetime, interval: int):
	total_slots = get_total_slots(start, end, interval)

	def wrapper(appointment_start, appointment_end):

		appointment_start = datetime.combine(start.date(), appointment_start.time())
		appointment_end = datetime.combine(start.date(), appointment_end.time())

		start_index = int((appointment_start - start).total_seconds() // 60 // interval)
		end_index = int((appointment_end - start).total_seconds() // 60 // interval)
		return max(0, start_index), min(end_index, total_slots)

	return wrapper


def get_capacity_between_interval(params: CapacityCalculationParams):
	daily_capacities = []
	start_of_interval = params.start_date
	end_of_interval = params.end_date
	for date in rrule(DAILY, dtstart=start_of_interval, until=end_of_interval):
		tasks = params.tasks
		intervals = params.intervals
		daily_intervals = [interval for interval in intervals if interval.start.weekday() == date.weekday()]
		daily_tasks = [task for task in tasks if task.start.date() == date.date()]

		daily_capacity = get_daily_capacity(date, daily_intervals, daily_tasks)
		daily_capacities.append(daily_capacity)

	return daily_capacities


def get_daily_capacity(date, intervals, tasks):
	daily_capacity = {
		'date': date.strftime('%Y-%m-%d'),
	}

	# Get morning capacity
	morning_capacity = get_morning_capacity(intervals, tasks)
	daily_capacity['morning_capacity'] = morning_capacity

	# Get afternoon capacity
	afternoon_capacity = get_afternoon_capacity(intervals, tasks)
	daily_capacity['afternoon_capacity'] = afternoon_capacity

	return daily_capacity


def get_morning_capacity(intervals, tasks):
	return get_capacity(intervals, tasks, 9, 13, 30)


def get_afternoon_capacity(intervals, tasks):
	return get_capacity(intervals, tasks, 13, 18, 30)


def get_capacity(intervals, tasks, start_hour: int, end_hour: int, step: int):
	available_slots = {

	}

	for interval in intervals:
		# Get morning slots
		start = interval.start
		end = interval.end
		worker_id = interval.worker_id
		if start.hour > end_hour or end.hour < start_hour:
			continue
		else:
			if end.hour > end_hour:
				end = end.replace(hour=end_hour, minute=0, second=0)
			if start.hour < start_hour:
				start = start.replace(hour=start_hour, minute=0, second=0)
			available_slots[worker_id] = get_total_slots(start, end, step) * [0]
			# Get morning appointments for this employee
			worker_tasks = [task for task in tasks if task.worker == worker_id]
			index_converter = convert_time(start, end, step)
			for task in worker_tasks:
				task_start = task.start
				task_end = task.end
				if task_start.hour > end_hour or task_end.hour < start_hour:
					continue
				start_index, end_index = index_converter(task_start, task_end)
				available_slots[worker_id][start_index:end_index + 1] = [1] * (end_index - start_index + 1)

	# Get morning capacity
	# Number of items in available_slots
	sum_of_items = 0
	number_of_items = 0
	for value in available_slots.values():
		sum_of_items += sum(value)
		number_of_items += len(value)

	if number_of_items == 0:
		return 1

	else:
		return sum_of_items / number_of_items
