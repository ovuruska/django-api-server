from datetime import datetime

from scheduling.models import Branch, Appointment


def get_branch_by_name(branch_name):
	"""
	:param branch_name: name of the branch
	:return: branch
	"""
	return Branch.objects.get(name=branch_name)


def get_free_hours(branch_id,date):

	start = datetime.strptime(date, '%Y-%m-%d').date()
	day_start = datetime.combine(start, datetime.min.time())
	day_end = datetime.combine(start, datetime.max.time())
	appointments = Appointment.objects.filter(branch_id=branch_id, start__gt=day_start,start__lte=day_end)

	appointments = appointments.order_by('start')
	available_hours = [8+i for i in range(12)]
	for appointment in appointments:
		start_hour = appointment.start.hour
		end_hour = appointment.end.hour
		for i in range(start_hour,end_hour):
			if i in available_hours:
				available_hours.remove(i)
	return [
		datetime.combine(start, datetime.min.time()).replace(hour=hour)
		for hour in available_hours
	]