from datetime import datetime, timedelta

from django.apps import apps
from django.forms import model_to_dict
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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


class BranchRetrieveModifyAPIView(RetrieveAPIView, ListAPIView, DestroyAPIView, UpdateAPIView):
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
	queryset = EmployeeWorkingHours.objects.all()

	@swagger_auto_schema(operation_id="getBranchEmployees", query_parameters=[
		openapi.Parameter(name='date', in_=openapi.IN_QUERY,
			description='Date for which the branch employees are requested. Format: YYYY-MM-DD',
			type=openapi.TYPE_STRING, required=True)],
		operation_description="Retrieve employees working at a specific branch on a given date.", responses={
			200: openapi.Response(description="Branch Employees", examples={"application/json": [
				{"id": 1, "name": "John Doe", "start": "09:00", "end": "17:00", "role": "Employee (We Wash)"},
				{"id": 2, "name": "Jane Smith", "start": "10:00", "end": "18:00", "role": "Employee (We Wash)"}]})})
	def get(self, request, *args, **kwargs):
		branch_id = self.kwargs['pk']
		date = request.query_params.get('date', None)

		if date is None:
			return Response(status=400)

		date = datetime.strptime(date, "%Y-%m-%d")
		employees = get_branch_employees(branch_id, date)

		return Response(data=employees, status=200)


class BranchDailyInformationAPIView(RetrieveAPIView):
	queryset = Branch.objects.all()

	@swagger_auto_schema(operation_id="getBranchDailyInformation", query_parameters=[
		openapi.Parameter(name='date', in_=openapi.IN_QUERY,
			description='Date for which the daily information is requested. Format: YYYY-MM-DD',
			type=openapi.TYPE_STRING, required=True)],
		operation_description="Retrieve daily information for a specific branch, including employees and appointments.",
		responses={200: openapi.Response(description="Average service time", examples={"application/json": {
			"employees": [
				{"id": 1, "name": "John Doe", "phone": "555-123-4567", "email": "john.doe@example.com", "role": 1,
				 "uid": "abc123"}], "appointments": [{"id": 1, "customer": {"id": 1, "name": "Jane Smith",
			                                                                "phone": "555-987-6543",
			                                                                "email": "jane.smith@example.com"},
			                                          "dog": {"id": 1, "name": "Buddy", "breed": "Golden Retriever",
			                                                  "birthdate": "2015-06-01"},
			                                          "start": "2023-05-01T10:00:00", "end": "2023-05-01T12:00:00",
			                                          "customer_notes": "Buddy has sensitive skin.",
			                                          "employee_notes": "Use hypoallergenic shampoo.",
			                                          "services": [{"id": 1, "name": "Full Grooming", "price": 50.00}],
			                                          "tip": 10.00, "cost": 60.00,
			                                          "products": [{"id": 1, "name": "Dog Shampoo", "price": 15.00}],
			                                          "branch": {"id": 1, "name": "Main Branch",
			                                                     "address": "123 Main St",
			                                                     "description": "Our main branch location.",
			                                                     "phone": "555-123-4567", "email": "main@example.com"},
			                                          "employee": {"id": 1, "name": "John Doe", "phone": "555-123-4567",
			                                                       "email": "john.doe@example.com", "role": 1,
			                                                       "uid": "abc123"}, "status": "Pending",
			                                          "appointment_type": "We Wash",
			                                          "reminder_sent": "2023-04-30T12:00:00", "check_in": None,
			                                          "pick_up": None, "confirmed_on": None, "checkout_time": None,
			                                          "checkout_status": False}]}})})
	def get(self, request, *args, **kwargs):
		branch_id = self.kwargs['pk']
		date = request.query_params.get('date', None)

		if date is None:
			return Response(status=400)

		date = datetime.strptime(date, "%Y-%m-%d")
		result = get_branch_daily_information(branch_id, date)

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
			all_working_hours = EmployeeWorkingHour.objects.filter(branch_id__in=branches,
			                                                       week_day=date.date().weekday())
			for wh in all_working_hours:
				if wh.employee.role != desired_role:
					continue

				employee = wh.employee
				branch = wh.branch

				start_time = datetime.combine(date.date(), wh.start)

				employee_appointments = Appointment.objects.filter(employee=employee, start__date=date.date()).order_by(
					"start")
				hours = [date, date + timedelta(minutes=1)]
				employee_appointments_times = [(appointment.start, appointment.end) for appointment in
				                               employee_appointments]
				slots = get_slots(hours, employee_appointments_times, 1)
				for slot in slots:
					if slot[0] <= date <= slot[1]:
						available_employees.append({"employee": BranchAvailableEmployeesEmployeeSerializer(employee),
						                            "branch": BranchAvailableEmployeesBranchSerializer(branch)})

		return Response(data=available_employees, status=200)
