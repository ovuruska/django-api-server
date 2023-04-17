from datetime import datetime, timedelta

from django.apps import apps
from django.forms import model_to_dict
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.response import Response

from common.get_slots import get_slots
from common.roles import Roles
from scheduling.models import Branch, EmployeeWorkingHour, Appointment
from scheduling.selectors.working_hours import get_branch_employees, get_branch_daily_information
from scheduling.serializers.Branch import BranchSerializer, BranchAvailableEmployeesBranchSerializer
from scheduling.serializers.Employee import BranchAvailableEmployeesEmployeeSerializer

class BranchListAllAPIView(ListAPIView):
	serializer_class = BranchSerializer
	queryset = Branch.objects.all()

class BranchRetrieveModifyAPIView(RetrieveAPIView,ListAPIView,DestroyAPIView,UpdateAPIView):
	serializer_class = BranchSerializer
	queryset = Branch.objects.all()

	def get(self, request, *args, **kwargs):
		if self.kwargs['pk'] == 'all':
			return self.list(request, *args, **kwargs)
		else:
			return self.retrieve(request, *args, **kwargs)

class BranchCreateAPIView(CreateAPIView):
	serializer_class = BranchSerializer
	queryset = Branch.objects.all()


class BranchEmployeesAPIView(ListAPIView):
	EmployeeWorkingHours = apps.get_model('scheduling', 'EmployeeWorkingHour')

	def get(self, request, *args, **kwargs):
		branch_id = self.kwargs['pk']
		date = request.query_params.get('date', None)

		if date is None:
			return Response(status=400)

		date = datetime.strptime(date, "%Y-%m-%d")
		employees = get_branch_employees(branch_id,date)

		return Response(data=employees, status=200)

class BranchDailyInformationAPIView(RetrieveAPIView):

	def get(self, request, *args, **kwargs):
		branch_id = self.kwargs['pk']
		date = request.query_params.get('date', None)

		if date is None:
			return Response(status=400)

		date = datetime.strptime(date, "%Y-%m-%d")
		result = get_branch_daily_information(branch_id,date)

		return Response(data=result, status=200)

class BranchAvailableEmployees(CreateAPIView):

	def post(self, request, *args, **kwargs):
		date_str = request.data.get('date', None)
		branches = request.data.get('branches', None)
		service = request.data.get('service', None)
		date = datetime.strptime(date_str, "%d-%m-%Y %H:%M")
		desired_role = None


		if date is None or service is None:
			return Response(status=400)

		if branches is None:
			branches = Branch.objects.all()

		if service == "Full Grooming":
			desired_role = Roles.EMPLOYEE_FULL_GROOMING
		elif service == "We Wash":
			desired_role = Roles.EMPLOYEE_WE_WASH

		available_employees = []
		for branch in branches:
			all_working_hours = EmployeeWorkingHour.objects.filter(branch_id__in=branches, week_day=date.date().weekday())
			for wh in all_working_hours:
				if wh.employee.role != desired_role:
					continue

				employee = wh.employee
				branch = wh.branch

				start_time = datetime.combine(date.date(), wh.start)


				employee_appointments = Appointment.objects.filter(
					employee=employee, start__date=date.date()
				).order_by("start")
				hours = [
					date,
					date + timedelta(minutes=1)
				]
				employee_appointments_times = [(appointment.start, appointment.end) for appointment in employee_appointments]
				slots = get_slots(hours, employee_appointments_times, 1)
				for slot in slots:
					if slot[0] <= date <= slot[1]:
						available_employees.append({
							"employee": BranchAvailableEmployeesEmployeeSerializer(employee),
							"branch": BranchAvailableEmployeesBranchSerializer(branch)
						})


		return Response(data=available_employees, status=200)

