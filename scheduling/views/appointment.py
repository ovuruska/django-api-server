from datetime import datetime, timedelta
from decimal import *

from django.apps import apps
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.signing import Signer
from django.db.models import Q
from django.http import QueryDict
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from common.get_slots import get_slots
from common.pagination import pagination
from common.permissions.AppointmentPermissions import CanCreateAppointment, CanUpdateAppointment, \
	CanAppointmentEmployeeRetrieve
from common.roles import Roles
from common.save_transaction import save_transaction
from ..models import Customer, Service, Product, EmployeeWorkingHour, Employee, Branch
from ..selectors import get_last_appointment_by_same_customer
from ..serializers.Appointment import *
from ..services import create_pet_with_name
from ..services.customer import create_customer_with_name


class AppointmentEmployeeCreateAPIView(generics.CreateAPIView, PermissionRequiredMixin):
	permission_required = [CanCreateAppointment]
	Customer = apps.get_model('scheduling', 'Customer')
	Dog = apps.get_model('scheduling', 'Dog')
	serializer_class = AppointmentEmployeeCreateSerializer

	def post(self, request, *args, **kwargs):
		customer_name = request.data.get("customer_name")
		customer_email = request.data.get("customer_email", "")
		customer_phone = request.data.get("customer_phone", "")
		customer = create_customer_with_name(customer_name, email=customer_email, phone=customer_phone)

		dog_name = request.data.get("dog_name")
		dog_breed = request.data.get("dog_breed", "")
		dog = create_pet_with_name(customer, dog_name, breed=dog_breed)

		cost = 0
		products = request.data.get('products', [])
		for product_id in products:
			product = Product.objects.get(id=product_id)
			cost += product.cost

		tip = request.data.get('tip', 0)
		cost += tip

		# Allow mutations for request.data
		try:
			request.data._mutable = True
		except AttributeError:
			pass

		try:

			appointment = Appointment(start=request.data["start"], end=request.data["end"], customer=customer, dog=dog,
			                          employee_id=request.data["employee_id"], branch_id=request.data["branch_id"],
			                          status=Appointment.Status.CONFIRMED, cost=cost)
			appointment.save()
			# Return the appointment as JSON
			serializer = AppointmentEmployeeSerializer(appointment)
			return Response(serializer.data)
		except KeyError as e:
			return Response({"error": str(e)}, status=400)


class AppointmentCreateAPIView(generics.CreateAPIView, PermissionRequiredMixin):
	"""
	start: Datetime String in ISO 8601 format : https://www.iso.org/iso-8601-date-and-time-format.html
	"""
	permission_classes = [CanCreateAppointment]
	Customer = apps.get_model('scheduling', 'Customer')
	serializer_class = AppointmentCreateSerializer
	queryset = Appointment.objects.all()

	def post(self, request, *args, **kwargs):
		try:
			request.data._mutable = True
		except AttributeError:
			pass

		# get customer object
		if request.data.get("customer__id") is not None:
			customer = Customer.objects.get(id=request.data.get("customer__id"))
		else:
			customer = Customer.objects.get(uid=request.data["customer"])
			request.data["customer__id"] = customer.id
		request.data["customer"] = customer.id

		# calculate cost
		cost = Decimal('0.00')
		products = request.data.get('products', [])
		for product_id in products:
			product = Product.objects.get(id=product_id)
			cost += product.cost

		services = request.data.get('services', [])
		for service_id in services:
			service = Service.objects.get(id=service_id)
			cost += service.cost

		tip = Decimal(request.data.get('tip', 0))
		cost += tip

		request.data["cost"] = cost

		# get last appointment for the same dog and customer
		last_dog_appointment = get_last_appointment_by_same_dog(request.data["dog"], request.data.get("start"))
		last_customer_appointment = get_last_appointment_by_same_customer(customer.id)
		if last_dog_appointment is not None:
			request.data["last_dog_appointment"] = last_dog_appointment.start
		if last_customer_appointment is not None:
			request.data["last_customer_appointment"] = last_customer_appointment.start

		to = customer.email

		title = "Scrubbers - Appointment Confirmation"
		signer = Signer()
		response = self.create(request, *args, **kwargs)
		appointment = response.data
		token = signer.sign(appointment["id"])
		accept_url = f"http://localhost:8000/api/confirmation/{token}/approve"
		cancel_url = f"http://localhost:8000/api/confirmation/{token}/cancel"
		reschedule_url = f"http://localhost:8000/api/confirmation/{token}/reschedule"
		start = appointment["start"]
		datetime_value = datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")
		date = datetime_value.strftime("%m/%d/%Y")
		hours = datetime_value.strftime("%I:%M %p")

		# body = approval_email(date, hours,accept_url, cancel_url, reschedule_url)
		# send_email(to,title,body)

		return response


class AppointmentModifyAPIView(generics.RetrieveAPIView, generics.UpdateAPIView, PermissionRequiredMixin):
	"""
	This view will be used in employee application to update the status of the appointment.
	"""
	permission_classes = [CanUpdateAppointment]
	serializer_class = AppointmentModifySerializer
	queryset = Appointment.objects.all()

	def get_queryset(self):
		return self.queryset.filter(id=self.kwargs['pk'])

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


class AppointmentEmployeeRetrieveAPIView(generics.RetrieveAPIView, PermissionRequiredMixin):
	permission_classes = [CanAppointmentEmployeeRetrieve]
	serializer_class = AppointmentEmployeeSerializer
	queryset = Appointment.objects.all()

	def get_queryset(self):
		return self.queryset.filter(id=self.kwargs['pk'])


class AppointmentCustomerRetrieve(generics.RetrieveAPIView):
	serializer_class = AppointmentCustomerRetrieveSerializer
	queryset = Appointment.objects.all()

	def get_queryset(self):
		return self.queryset.filter(id=self.kwargs['pk'])


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
