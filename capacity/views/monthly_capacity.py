from datetime import datetime

from django.apps import apps
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from django.db.models import Q

from capacity.selectors.monthly_capacity import get_monthly_capacity
from capacity.serializers.requests.monthly_capacity import MonthlyCapacityRequestSerializer
from capacity.serializers.responses.monthly_capacity import MonthlyCapacityResponseSerializer
from common.roles import Roles
from common.validate_request import validate_request
from scheduling.models import EmployeeWorkingHour

Employee = apps.get_model('scheduling', 'Employee')
Branch = apps.get_model('scheduling', 'Branch')

class GetMonthlyCapacity(APIView):
	permission_classes = (IsAuthenticated,)
	@validate_request(MonthlyCapacityRequestSerializer)
	def post(self, request, *args, **kwargs):
		date = request.data['date']
		service = request.data['service']
		if service == "Full Grooming":
			role = Roles.EMPLOYEE_FULL_GROOMING
		else:
			role = Roles.EMPLOYEE_WE_WASH

		branches = request.data.get('branches', [])
		employees = request.data.get('employees', [])
		if not branches and not employees:
			employees = Employee.objects.filter(role=role).values_list('id', flat=True)

		if employees:
			employees = Employee.objects.filter(role=role,id__in=employees).values_list('id', flat=True)

		if branches:
			branch_employees = EmployeeWorkingHour.objects.filter(
				Q(branch_id__in=branches)).values_list('employee_id',flat=True).distinct()
			branch_employees = Employee.objects.filter(role=role,id__in=branch_employees).values_list('id', flat=True)

			employees = list(set(employees).union(set(branch_employees)) )


		date = datetime.strptime(date, '%m/%Y')


		monthly_capacity = get_monthly_capacity(date, employees)
		serializer = MonthlyCapacityResponseSerializer(data=monthly_capacity, many=True)
		serializer.is_valid(raise_exception=True)
		return JsonResponse(serializer.data, status=HTTP_200_OK, safe=False)