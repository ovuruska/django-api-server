import datetime

from django.apps import apps
from django.forms import model_to_dict

from common.datetime_range import datetime_range

def get_branch_working_hours(start,end,branch_id) -> [str]:
	BranchWorkingHour = apps.get_model('scheduling','BranchWorkingHour')

	branch_working_hours = BranchWorkingHour.objects.filter(branch=branch_id)
	working_hours = []
	start = datetime.datetime.strptime(start, "%Y-%m-%d")
	end = datetime.datetime.strptime(end, "%Y-%m-%d")

	for date in datetime_range(start, end):
		week_day = date.weekday()

		closest = branch_working_hours.filter(week_day=week_day).order_by('date').first()
		if closest == None:
			result = 24 * "0"
		else:
			result = closest.working_hours

		working_hours.append({
			"date": date,
			"working_hours": result
		})

	return working_hours

def set_branch_working_hours(branch_id,date, working_hours):
	BranchWorkingHour = apps.get_model('scheduling', 'BranchWorkingHour')
	date = datetime.datetime.strptime(date, "%Y-%m-%d")


	created = {
		"date": date,
		"week_day": date.weekday(),
		"working_hours": working_hours,
		"branch_id": branch_id

	}

	BranchWorkingHour.objects.filter(branch_id=branch_id, date=date).delete()
	BranchWorkingHour.objects.update_or_create(
		**created
	)

	return created


"""
	{
		"start": "2020-01-01",
		"end": "2020-01-31",
		"employee":Employee
		"working_hours":[
			{ 
				"working_hours":char[24],
				"branch":Branch,
				"date":date
			}
	}

"""
def decode_working_hours(working_hours:[str]) -> [bool]:
	return [bool(int(x)) for x in working_hours]

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
		if closest == None:
			result = 24 * "0"
			branch = None
		else:
			branch = closest.branch_id
			branch = Branch.objects.get(id=branch)
			branch = model_to_dict(branch)
			result = closest.working_hours

		working_hours.append({
			"date": date.strftime("%Y-%m-%d"),
			"branch":branch,
			"working_hours": decode_working_hours(result)
		})

	return working_hours


def set_employee_working_hours(employee_id, date, working_hours, branch_id):
	EmployeeWorkingHour = apps.get_model('scheduling', 'EmployeeWorkingHour')
	date = datetime.datetime.strptime(date, "%Y-%m-%d")
	created = {
		"employee_id": employee_id,
		"date": date,
		"week_day": date.weekday(),
		"working_hours": working_hours,
		"branch_id": branch_id

	}

	EmployeeWorkingHour.objects.filter(employee_id=employee_id, date=date).delete()
	EmployeeWorkingHour.objects.update_or_create(
		**created
	)

	return created

