import datetime

from django.apps import apps
from django.forms import model_to_dict

from common.datetime_range import datetime_range

def quantize(date: datetime.datetime):
	if(date.minute < 30):
		date = date.replace(minute=0)
	else:
		date = date.replace(minute=30)
	return date


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
	for date in datetime_range(start, end):
		week_day = date.weekday()

		# Order dates by descending order
		closest = employee_working_hours.filter(week_day=week_day).order_by('-date').first()
		start = None
		end = None
		if closest == None:
			result = 24 * "0"
			branch = None
		else:
			branch = closest.branch_id
			branch = Branch.objects.get(id=branch)
			branch = model_to_dict(branch)
			start = quantize(closest.start)
			end = quantize(closest.end)


		working_hours.append({
			"date": date.strftime("%Y-%m-%d"),
			"branch": branch,
			"start": start,
			"end": end,
		})

	return working_hours

def set_employee_working_hours(employee_id, date, start,end, branch_id):
	EmployeeWorkingHour = apps.get_model('scheduling', 'EmployeeWorkingHour')
	date = datetime.datetime.strptime(date, "%Y-%m-%d")

	EmployeeWorkingHour.objects.filter(employee_id=employee_id, date=date).delete()

	if branch_id != None:
		created = {
			"employee_id": employee_id,
			"date": date.replace(tzinfo=None),
			"week_day": date.weekday(),
			"start": datetime.datetime.fromisoformat(start).replace(tzinfo=None),
			"end":datetime.datetime.fromisoformat(end).replace(tzinfo=None),
			"branch_id": branch_id

		}
		EmployeeWorkingHour.objects.update_or_create(
			**created
		)
		return created

	else:
		return None
