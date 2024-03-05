from datetime import datetime, timedelta
from decimal import *

from django.apps import apps
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.signing import Signer
from django.db.models import Q
from django.http import QueryDict
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from common.get_slots import get_slots
from common.pagination import pagination
from common.permissions.AppointmentPermissions import CanCreateAppointment, CanUpdateAppointment, \
	CanAppointmentEmployeeRetrieve
from common.roles import Roles
from common.save_transaction import save_transaction
from common.validate_request import validate_request
from ..models import Customer, Service, Product, EmployeeWorkingHour, Employee, Branch
from ..selectors import get_last_appointment_by_same_customer
from ..serializers.Appointment import *
from ..services import create_pet_with_name
from ..services.customer import create_customer_with_name


class AppointmentEmployeeCreateAPIView(generics.CreateAPIView):
	Customer = apps.get_model('scheduling', 'Customer')
	Dog = apps.get_model('scheduling', 'Dog')
	serializer_class = AppointmentEmployeeSerializer

	@swagger_auto_schema(
		request_body=AppointmentEmployeeCreateSerializer,
		operation_description="Create an appointment",
		responses={201: AppointmentEmployeeSerializer}
	)
	@validate_request(AppointmentEmployeeCreateSerializer)
	def post(self, request, *args, **kwargs):

		customer = request.data.get('customer')
		pet = request.data.get('pet')
		employee = request.data.get('employee')
		branch = request.data.get('branch')


		cost = 0
		products = request.data.get('products', [])
		for product_id in products:
			product = Product.objects.get(id=product_id)
			cost += Decimal(product.cost)

		tip = request.data.get('tip', 0)
		cost += tip

		start = request.data["start"]
		end = request.data.get("end",None)
		if end is None:
			# Convert start to date time with day month hour
			start_datetime = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
			end = start_datetime + timedelta(hours=1)

		appointment = Appointment(start=request.data["start"], end=end, customer_id=customer, dog_id=pet,
		                          employee_id=employee, branch_id=branch
		                          ,
		                          status=Appointment.Status.CONFIRMED, cost=cost)
		appointment.save()
		# Return the appointment as JSON
		serializer = AppointmentEmployeeSerializer(appointment)
		return Response(serializer.data,status = HTTP_201_CREATED)

class AppointmentModifyAPIView(generics.RetrieveAPIView, generics.UpdateAPIView):
	"""
	This view will be used in employee application to update the status of the appointment.
	"""
	serializer_class = AppointmentModifySerializer
	queryset = Appointment.objects.all()

	def get_queryset(self):
		if 'pk' in self.kwargs:
			return self.queryset.filter(id=self.kwargs['pk'])
		return self.queryset.none()

	def get(self, request, *args, **kwargs):
		"""
		Returns the appointment with the given id
		"""
		pk = self.kwargs.get("pk")
		appointment = Appointment.objects.get(id=pk)
		serializer = AppointmentEmployeeSerializer(appointment)
		return Response(serializer.data)

	@save_transaction
	def patch(self, request, *args, **kwargs):
		"""
		Updates the appointment with the given id
		"""
		pk = self.kwargs.get("pk")
		appointment = Appointment.objects.get(id=pk)

		if not appointment.is_modifiable():
			return Response({"error": "Cannot modify a completed appointment"}, status=400,
			                content_type="application/json")

		# Update the appointment with the new data
		serializer = AppointmentModifySerializer(appointment, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		appointment = serializer.save()

		# Recalculate the cost based on the new services and products, as well as the tip
		cost = 0
		tip = request.data.get('tip', 0)



		# Add cost of new products
		new_products = request.data.get('products', [])
		for product in new_products:
			cost += product.cost


		# Add tip to total cost
		cost += tip

		# Update the appointment with the new cost
		appointment.cost = cost
		appointment.save()

		serializer = AppointmentEmployeeSerializer(appointment)
		return Response(serializer.data)


class AppointmentEmployeeRetrieveAPIView(generics.RetrieveAPIView):
	serializer_class = AppointmentEmployeeSerializer
	queryset = Appointment.objects.all()

	def get_queryset(self):
		if 'pk' in self.kwargs:
			return self.queryset.filter(id=self.kwargs['pk'])
		return self.queryset.none()


class CustomerGetAppointmentsAPIView(generics.ListAPIView):
	serializer_class = AppointmentModifySerializer

	def get_queryset(self):
		# Get the authenticated user's customer object
		try:
			customer = self.request.user.customer
		except Customer.DoesNotExist:
			return Appointment.objects.none()

		# Get the customer's appointments
		appointments = customer.appointments.all()

		# Apply filters
		start_date = self.request.query_params.get('start__gt')
		if start_date:
			appointments = appointments.filter(start__gt=start_date)

		end_date = self.request.query_params.get('start__lt')
		if end_date:
			appointments = appointments.filter(start__lt=end_date)

		appointments = pagination(self.request, appointments)
		return appointments


class EmployeeFreeTimesAPIView(generics.CreateAPIView, PermissionRequiredMixin):
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):
		if not request.data:
			return Response({"error": "No data provided"}, status=400,
			                content_type="application/json")


		if isinstance(request.data, QueryDict):
			branches = [int(val) for val in request.data.getlist("branches",[])]
			employees_param = [int(val) for val in request.data.getlist("employees", [])]

		else:
			branches = request.data.get("branches",[])
			employees_param = request.data.get("employees",[])


		date_str = request.data.get("date")

		try:
			date = datetime.strptime(date_str, "%Y-%m-%d")

			if date < datetime.now() - timedelta(days=1):
				return Response({"error": "Cannot schedule an appointment in the past"}, status=400,
				                content_type="application/json")
		except ValueError:
			return Response({"error": "Invalid date format"}, status=400,
			                content_type="application/json")

		duration = int(request.data.get("duration"))
		service_type = request.data.get("service")
		role = Roles.ANONYMOUS

		if service_type == "Full Grooming":
			role = Roles.EMPLOYEE_FULL_GROOMING
		elif service_type == "We Wash":
			role = Roles.EMPLOYEE_WE_WASH



		if not branches and  not employees_param:
			employees = Employee.objects.filter(role=role)
			branches = Branch.objects.all()
		else:
			if employees_param:
				employees = Employee.objects.filter(id__in=employees_param, role=role)
			else:
				employees = Employee.objects.none()

			if branches:
				branches = Branch.objects.filter(id__in=branches)
			else:
				branches = Branch.objects.none()


		all_working_hours = EmployeeWorkingHour.objects.filter(
			Q(employee_id__in=employees) | Q(branch_id__in=branches)
		)

		if not all_working_hours:
			return Response([], status=200,
			                content_type="application/json")

		free_times = []
		slot_num = 40  # it can be changed after. This number will determine the number of free times that will be displayed
		while len(free_times) != slot_num:

			working_hours = all_working_hours.filter(
				week_day=date.date().weekday(),
			)
			for working_interval in working_hours:
				employee = working_interval.employee
				branch = working_interval.branch


				start_time = datetime.combine(date.date(), working_interval.start)
				end_time = datetime.combine(date.date(), working_interval.end)

				employee_appointments = Appointment.objects.filter(
					employee=employee, start__date=date.date()
				).order_by("start")
				hours = [
					start_time,
					end_time
				]
				employee_appointments_times = [(appointment.start,appointment.end) for appointment in employee_appointments]
				slots = get_slots(hours, employee_appointments_times, duration)
				for slot_start,slot_end in slots:

					time_slot = {"branch": BranchSerializer(branch).data,
					             "employee": EmployeeSerializer(employee).data,
					             "start": slot_start.strftime("%Y-%m-%dT%H:%M:%S"),
					             "end": slot_end.strftime("%Y-%m-%dT%H:%M:%S"),
					             "date": date
					             }
					free_times.append(time_slot)
					if len(free_times) == slot_num:
						free_times.sort(key=lambda x: x["start"])
						return Response(free_times)


			new_date = date + timedelta(days=1)
			date = new_date  # assign the new datetime object back to date

		free_times.sort(key=lambda x: x["start"])

		return Response(free_times)
