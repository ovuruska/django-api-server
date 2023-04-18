from datetime import datetime

from django.apps import apps
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from available.selectors.daily_available import get_daily_available_slots
from available.serializers.requests.daily_view import DailyViewRequestSerializer
from available.serializers.responses.daily_view import DailyViewResponseSerializer
from common.roles import Roles
from common.validate_request import validate_request

Employee = apps.get_model('scheduling', 'Employee')
Appointment = apps.get_model('scheduling', 'Appointment')
EmployeeWorkingHour = apps.get_model('scheduling', 'EmployeeWorkingHour')


class DailyAvailableView(APIView):

	@validate_request(DailyViewRequestSerializer)
	def post(self, request, *args, **kwargs):
		serialized_data = kwargs['serialized_data']
		date = serialized_data['date']
		service = serialized_data['service']
		duration = serialized_data['duration']
		if service == "Full Grooming" or service == "Grooming":
			role = Roles.EMPLOYEE_FULL_GROOMING
		else:
			role = Roles.EMPLOYEE_WE_WASH

		branches = serialized_data['branches']
		employees = serialized_data['employees']

		if not branches and not employees:
			employees = Employee.objects.filter(role=role).values_list('id', flat=True)

		if employees:
			employees = Employee.objects.filter(role=role, id__in=employees).values_list('id', flat=True)

		if branches:
			branch_employees = EmployeeWorkingHour.objects.filter(
				Q(branch_id__in=branches)).values_list('employee_id', flat=True).distinct()
			branch_employees = Employee.objects.filter(role=role, id__in=branch_employees).values_list('id', flat=True)

			employees = list(set(employees).union(set(branch_employees)))

		start_of_day = datetime.combine(date, datetime.min.time())
		end_of_day = datetime.combine(date, datetime.max.time())
		appointments = Appointment.objects.filter(
			Q(employee_id__in=employees) & Q(start__gt=start_of_day) & Q(start__lt=end_of_day) )

		working_intervals = EmployeeWorkingHour.objects.filter(
			Q(employee_id__in=employees) & Q(week_day=date.weekday()))

		slots = get_daily_available_slots(working_intervals, appointments, duration,date)

		serializer = DailyViewResponseSerializer(data=slots, many=True)
		serializer.is_valid(raise_exception=True)
		return JsonResponse(serializer.data, status=HTTP_200_OK, safe=False)