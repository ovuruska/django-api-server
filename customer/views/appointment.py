from datetime import timedelta, timezone, datetime

from django.apps import apps
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from random import choice
from common.validate_request import validate_request
from customer.serializers.requests.appointment import CustomerAppointmentRequestSerializer
from customer.serializers.responses.appt_response import CustomerAppointmentResponseSerializer

Appointment = apps.get_model("scheduling", "Appointment")
EmployeeWorkingHours = apps.get_model("scheduling", "EmployeeWorkingHour")
Employee = apps.get_model("scheduling", "Employee")
Branch = apps.get_model("scheduling", "Branch")
Dog = apps.get_model("scheduling", "Dog")
Product = apps.get_model("scheduling", "Product")


class CustomerCreateAppointment(generics.CreateAPIView):
	serializer_class = CustomerAppointmentRequestSerializer
	permission_classes = [IsAuthenticated]

	@validate_request(CustomerAppointmentRequestSerializer)
	def create(self, request, *args, **kwargs):
		serialized_data = kwargs.get("serialized_data")
		customer = request.user.customer
		service = serialized_data.get("service")
		start = serialized_data.get("start")
		branch = Branch.objects.get(id=serialized_data.get("branch"))
		products = serialized_data.get("products", [])
		if service == "We Wash":

			week_day = start.weekday()
			start_hours = start.strftime("%H:%M")
			employees = EmployeeWorkingHours.objects.filter(
				branch=branch,
				week_day=week_day,
				start__lte=start_hours,
				end__gte=start_hours
			).values_list("employee", flat=True)
			employee_id = choice(employees)
			employee = Employee.objects.get(id=employee_id)
		else:
			employee = Employee.objects.get(id=serialized_data.get("employee"))

		end = start + timedelta(minutes=90)

		appointment = Appointment.objects.create(
			customer=customer,
			employee=employee,
			start=start,
			appointment_type=service,
			branch=branch,
			end=end,
			customer_notes=serialized_data.get("customer_notes", ""),
			dog=Dog.objects.get(id=serialized_data.get("pet")),

		)
		appointment.save()
		appointment.products.set(products)
		serializer = CustomerAppointmentResponseSerializer(appointment)
		return Response(serializer.data)


class CustomerCancelAppointment(generics.UpdateAPIView):
	serializer_class = CustomerAppointmentResponseSerializer
	permission_classes = [IsAuthenticated]
	#	path('appointment/cancel/<int:appointment_id>', CustomerCancelAppointment.as_view(), name="customer/appointment/cancel"),

	def get_queryset(self):
		customer = self.request.user.customer
		app_id = self.kwargs.get("appointment_id")

		return Appointment.objects.get(id=app_id, customer=customer)

	def update(self, request, *args, **kwargs):
		try:
			appt = self.get_queryset()
		except Appointment.DoesNotExist:
			return Response({"error": "Appointment not found"}, status=404)
		if appt is None:
			return Response({"error": "Appointment not found"}, status=404)
		if appt.status == "Cancelled":
			return Response({"error": "Appointment already cancelled"}, status=400)
		# Check if appointment has more than 24 hours to start.
		if appt.start - datetime.now(timezone.utc) < timedelta(hours=24):
			return Response({"error": "Appointment cannot be cancelled within 24 hours of start time"}, status=400)

		appt.status = "Cancelled"
		appt.save()
		serializer = CustomerAppointmentResponseSerializer(appt)
		return Response(serializer.data)