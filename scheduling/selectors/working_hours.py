import datetime

from django.apps import apps

from common.datetime_range import datetime_range


def get_employee_working_hours(start, end, employee_id) -> [str]:
	EmployeeWorkingHour = apps.get_model('scheduling', 'EmployeeWorkingHour')

	employee_working_hours = EmployeeWorkingHour.objects.filter(employee=employee_id)
	working_hours = []
	start = datetime.datetime.strptime(start, "%Y-%m-%d")
	end = datetime.datetime.strptime(end, "%Y-%m-%d")
	for date in datetime_range(start, end):
		week_day = date.weekday()

		closest = employee_working_hours.filter(week_day=week_day).order_by('date').first()
		if closest == None:
			result = 24 * "0"
		else:
			result = closest.working_hours

		working_hours.append({
			"date": date,
			"working_hours": result
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

