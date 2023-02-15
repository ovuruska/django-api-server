from datetime import datetime

from django.apps import apps
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.signing import Signer
from rest_framework import generics
from rest_framework.response import Response

from common.permissions.AppointmentPermissions import CanCreateAppointment, CanUpdateAppointment, \
	CanAppointmentEmployeeRetrieve
from ..models import Customer
from ..selectors import get_last_appointment_by_same_customer
from ..serializers.Appointment import *


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

		if request.data.get("customer__id") is not None:
			customer = Customer.objects.get(id=request.data.get("customer__id"))
		else:
			customer = Customer.objects.get(uid=request.data["customer"])
			request.data["customer__id"] = customer.id

		request.data["customer"] = customer.id

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


class AppointmentModifyAPIView(generics.UpdateAPIView, PermissionRequiredMixin):
	"""
	This view will be used in employee application to update the status of the appointment.
	"""
	permission_classes = [CanUpdateAppointment]
	serializer_class = AppointmentModifySerializer
	queryset = Appointment.objects.all()

	def get_queryset(self):
		return self.queryset.filter(id=self.kwargs['pk'])

	def patch(self, request, *args, **kwargs):
		"""
		Updates the appointment with the given id
		"""
		pk = self.kwargs.get("pk")
		appointment = Appointment.objects.get(id=pk)
		if not appointment.is_modifiable():
			return Response({"error": "Cannot modify a completed appointment"}, status=400,
			                content_type="application/json")
		self.partial_update(request, *args, **kwargs)
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
