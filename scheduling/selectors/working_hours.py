import datetime

from django.apps import apps
from django.db.models import Q
from django.forms import model_to_dict

from common.datetime_range import datetime_range
from common.extract_role import get_role, get_role_from_int


def quantize(date: datetime.datetime):
	if(date.minute < 30):
		date = date.replace(minute=0)
	else:
		date = date.replace(minute=30)
	return date.replace(tzinfo=None)


def get_branch_working_hours(start, end, branch_id) -> [str]:
	BranchWorkingHour = apps.get_model('scheduling', 'BranchWorkingHour')

	branch_working_hours = BranchWorkingHour.objects.filter(branch=branch_id)
	working_hours = []
	start = datetime.datetime.strptime(start, "%Y-%m-%d")
	end = datetime.datetime.strptime(end, "%Y-%m-%d")

	for date in datetime_range(start, end):
		week_day = date.weekday()

		closest = branch_working_hours.filter(week_day=week_day).order_by('date').first()
		start = None
		end = None
		if closest is not None:
			start = quantize(closest.start)
			end = quantize(closest.end)

		working_hours.append({
			"date": date,
			"start": start,
			"end": end,
		})

	return working_hours


def set_branch_working_hours(branch_id, date, start,end):


	BranchWorkingHour = apps.get_model('scheduling', 'BranchWorkingHour')
	date = datetime.datetime.strptime(date, "%Y-%m-%d")

	created = {
		"date": date,
		"week_day": date.weekday(),
		"start": datetime.datetime.fromisoformat(start).replace(tzinfo=None),
		"end": datetime.datetime.fromisoformat(end).replace(tzinfo=None),
		"branch_id": branch_id,
	}

	BranchWorkingHour.objects.filter(branch_id=branch_id, date=date).delete()
	BranchWorkingHour.objects.update_or_create(
		**created
	)

	return created


def get_employee_working_hours(start, end, employee_id) -> [str]:
	EmployeeWorkingHour = apps.get_model('scheduling', 'EmployeeWorkingHour')
	Branch = apps.get_model(
		'scheduling',
		'Branch'
	)

	employee_working_hours = EmployeeWorkingHour.objects.filter(employee=employee_id)
	working_hours = []
	for start in datetime_range(start, end):
		week_day = start.weekday()

		# Order dates by descending order
		closest = employee_working_hours.filter(week_day=week_day).order_by('-start').first()
		start = None
		end = None
		if closest == None:
			branch = None
		else:
			branch = closest.branch_id
			branch = Branch.objects.get(id=branch)
			branch = model_to_dict(branch)
			start = quantize(closest.start) if closest.start is not None else None
			end = quantize(closest.end) if closest.end is not None else None


		working_hours.append({
			"branch": branch,
			"start": start,
			"end": end,
		})

	return working_hours

def set_employee_working_hours(employee_id, start, end, branch_id):
	EmployeeWorkingHour = apps.get_model('scheduling', 'EmployeeWorkingHour')
	start = datetime.datetime.strptime(start, "%Y-%m-%d")
	end = datetime.datetime.strptime(end, "%Y-%m-%d")

	EmployeeWorkingHour.objects.filter(employee_id=employee_id, start=start).delete()

	if branch_id != None:
		created = {
			"employee_id": employee_id,
			"week_day": start.weekday(),
			"start": start,
			"end":end,
			"branch_id": branch_id

		}
		EmployeeWorkingHour.objects.update_or_create(
			**created
		)
		return created

	else:
		return None

def get_branch_daily_information(branch_id:int, date:datetime.datetime):
	branch_id = int(branch_id)
	employees = get_branch_employees(branch_id,date)
	employee_ids = list(map(lambda x:x["id"],employees))
	appointments = get_branch_appointments(branch_id, date,employee_ids)
	return {
		"employees": employees,
		"appointments": appointments
	}
def get_branch_appointments(branch_id:int, date:datetime.datetime,employees):
	Appointment = apps.get_model('scheduling', 'Appointment')
	start_range = datetime.datetime(date.year, date.month, date.day, 0, 0, 0)
	end_range = start_range + datetime.timedelta(days=1)
	# 2023-03-19
	start = start_range.strftime("%Y-%m-%d")
	end = end_range.strftime("%Y-%m-%d")
	appointments = Appointment.objects.filter(
		Q(branch_id=branch_id, start__lt = end, start__gt = start) | Q(employee__in = employees, start__lt = end, start__gt = start))

	return [appointment.to_dict() for appointment in appointments]

def get_branch_employees(branch_id:int,date : datetime.datetime):
	branch_id = int(branch_id)
	EmployeeWorkingHour = apps.get_model('scheduling', 'EmployeeWorkingHour')

	week_day = date.weekday()
	working_hours = EmployeeWorkingHour.objects.filter(branch_id=branch_id,week_day=week_day)

	results = []

	for working_interval in working_hours:
		employee = working_interval.employee
		start = working_interval.start
		end = working_interval.end
		employee_dict = {
			"id": employee.id,
			"name": employee.name,
			"start": start,
			"end": end,
			"role": get_role_from_int(employee.role),

		}
		results.append(employee_dict)

	return results

