from datetime import datetime

from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from capacity.selectors.daily_capacity import get_daily_capacity_list
from capacity.selectors.utils import get_daily_capacity
from capacity.serializers.requests.daily_capacity import DailyCapacityRequestSerializer
from capacity.serializers.responses.daily_capacity import DailyCapacityResponseSerializer
from common.roles import Roles
from common.validate_request import validate_request
from scheduling.models import Employee, EmployeeWorkingHour


class GetDailyCapacityView(APIView):
	@validate_request(DailyCapacityRequestSerializer)
	def post(self, request, *args, **kwargs):
		date = request.data['date']
		service = request.data['service']
		if service == "Full Grooming":
			role = Roles.EMPLOYEE_FULL_GROOMING
		else:
			role = Roles.EMPLOYEE_WE_WASH

		branches = request.data.get('branches', [])
		employees = request.data.get('employees', [])

		if employees:
			employees = Employee.objects.filter(role=role,id__in=employees).values_list('id', flat=True)

		# Aggregate branches from employee working hours.


		employee_branches = set( EmployeeWorkingHour.objects.filter(
			Q(employee_id__in=employees) | Q(branch_id__in=branches)).values_list('branch_id', flat=True))


		date = datetime.strptime(date, '%Y-%m-%d')
		daily_capacities = get_daily_capacity_list(date, list(employee_branches),employees)
		serializer = DailyCapacityResponseSerializer(data=daily_capacities, many=True)
		serializer.is_valid(raise_exception=True)
		return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)