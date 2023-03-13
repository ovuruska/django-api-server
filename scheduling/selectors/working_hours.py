import datetime

from django.apps import apps
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

def get_branch_employees(branch_id,date):
	branch_id = int(branch_id)
	Employee = apps.get_model('scheduling', 'Employee')
	employees = []
	for employee in Employee.objects.all():
		start = datetime.datetime.strptime(date, "%Y-%m-%d")
		end = start + datetime.timedelta(days=1)
		working_hours = get_employee_working_hours(start, end, employee.id)
		working_hours = working_hours[0]
		if working_hours["branch"] is not None and working_hours["branch"]["id"] == branch_id and working_hours["start"] is not None and working_hours["end"] is not None:
			employee.work_start = working_hours["start"]
			employee.work_end = working_hours["end"]
			employee_dict = {
				"id": employee.id,
				"name": employee.name,
				"start": employee.work_start,
				"end": employee.work_end,
				"role": get_role_from_int(employee.role),

			}
			employees.append(employee_dict)
	return employees

