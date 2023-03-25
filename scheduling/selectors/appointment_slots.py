import datetime

from common.roles import Roles
from scheduling.models import EmployeeWorkingHour, Appointment, Employee


def get_daily_slots(hours, appointments, duration=datetime.timedelta(hours=1)):
	"""
	appointments = [(datetime(2012, 5, 22, 10), datetime(2012, 5, 22, 10, 30)),
				(datetime(2012, 5, 22, 12), datetime(2012, 5, 22, 13)),
				(datetime(2012, 5, 22, 15, 30), datetime(2012, 5, 22, 17, 10))]

	hours = (datetime(2012, 5, 22, 9), datetime(2012, 5, 22, 18))
	"""
	daily_slots = []
	slots = sorted([(hours[0], hours[0])] + appointments + [(hours[1], hours[1])])
	for start, end in ((slots[i][1], slots[i + 1][0]) for i in range(len(slots) - 1)):
		assert start <= end, "Cannot attend all appointments"
		while start + duration <= end:
			slot_start, slot_end = start, start + duration
			daily_slots.append((slot_start, slot_end))
			start += duration

	return daily_slots

def get_available_appointment_slots(employees, branches, start_date: datetime.datetime, service_type, duration,
                                    page_count=50):
	"""
	Returns a list of available appointment slots for the given employees and branches
	:param employees: A list of employee ids
	:param branches: A list of branch ids
	:param start_date: The start date of the appointment
	:param service_type: The type of service
	:return: A list of available appointment slots
	"""
	# Get the employee working hours for the given date

	if employees == [] and branches == []:
		return get_all_available_slots(start_date, service_type, page_count)

def get_all_available_slots(start_date: datetime.datetime, service_type, page_count=50):

	current_date = start_date
	available_slots = []
	role = Roles.get_role_choices(service_type)
	employees = Employee.objects.filter(role=role)

	if len(employees) == 0:
		return available_slots


	while len(available_slots) <= page_count:
		end = current_date + datetime.timedelta(days=1)
		day = start_date.day
		employee_working_hours = EmployeeWorkingHour.objects.filter(
			employee__in=employees,
			week_day=day,
		)
		for employee_working_hour in employee_working_hours:
			# Get the appointments for the given employee and date
			appointments = Appointment.objects.filter(
				employee=employee_working_hour.employee,
				start__gt=current_date,
				start__lt=end
			).order_by("start").only("start", "end")
			# Get the available slots
			available_slots += get_daily_slots(
				(employee_working_hour.start.time(), employee_working_hour.end.time()),
				[(appointment.start.time(), appointment.end.time()) for appointment in appointments]
			)

		current_date = end
