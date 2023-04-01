import datetime


class IntervalEntity:
	def __init__(self, start :datetime.datetime, end: datetime.datetime):
		# Disable tz aware
		self.start: datetime.datetime = start.replace(tzinfo=None).replace(microsecond=0,second=0)
		self.end: datetime.datetime = end.replace(tzinfo=None).replace(microsecond=0,second=0)

	def __lt__(self, other):
		return self.start < other.start

	def __gt__(self, other):
		return self.start > other.start

	def __eq__(self, other):
		return self.start == other.start





def get_slots(working_interval: IntervalEntity, appointments: [IntervalEntity], minutes=60, step=30):
	duration = datetime.timedelta(minutes=minutes)
	step = datetime.timedelta(minutes=step)
	available_slots = []

	appointments = sorted(appointments)
	appointments_tuple = [(appointment.start, appointment.end) for appointment in appointments]
	slots = sorted([(working_interval.start, working_interval.start)] + appointments_tuple + [
		(working_interval.end, working_interval.end)])
	for start, end in ((slots[i][1], slots[i + 1][0]) for i in range(len(slots) - 1)):
		while start + duration <= end:
			available_slots.append((start, start + duration))
			start += step

	return available_slots


def get_daily_available_slots(working_hours, appointments, duration, date: datetime.datetime):
	all_slots = []

	working_intervals = [IntervalEntity(start=datetime.datetime.combine(date, working_hour.start),
	                                    end=datetime.datetime.combine(date, working_hour.end)) for working_hour in
	                     working_hours]
	grouped_appointments = [
		[
			IntervalEntity(start=appointment.start, end=appointment.start)
			for appointment in appointments
			if appointment.employee_id == working_hour.employee_id
		] for working_hour in working_hours

	]

	for working_hour, working_interval, employee_appointments in zip(working_hours, working_intervals,
	                                                                 grouped_appointments):
		available_slots = get_slots(working_interval, employee_appointments, duration)
		all_slots.extend(
			[{'start': slot[0], 'end': slot[1], 'employee': working_hour.employee_id, 'branch': working_hour.branch_id}
			 for slot in available_slots])

	return all_slots
