from datetime import datetime

from django.core.signing import Signer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response

from templates.email import approval_email
from ..models import Customer
from ..serializers.Appointment import *
from ..services.send_email import send_email

class AppointmentCreateAPIView(generics.CreateAPIView):
	"""

	start: Datetime String in ISO 8601 format : https://www.iso.org/iso-8601-date-and-time-format.html
	"""

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

		request.data["customer"] = customer.id

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
		datetime_value = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
		date = datetime_value.strftime("%m/%d/%Y")
		hours = datetime_value.strftime("%I:%M %p")

		body = approval_email(date, hours,accept_url, cancel_url, reschedule_url)
		send_email(to,title,body)

		return response

class AppointmentModifyAPIView(generics.UpdateAPIView):
	"""
	This view will be used in employee application to update the status of the appointment.
	"""
	serializer_class = AppointmentEmployeeSerializer
	queryset = Appointment.objects.all()

	def patch(self, request, *args, **kwargs):
		"""
		Updates the appointment with the given id
		"""
		pk = self.kwargs.get("pk")
		appointment = Appointment.objects.get(id=pk)
		if not appointment.is_modifiable():
			return Response({"error": "Cannot modify a completed appointment"}, status=400,
			                content_type="application/json")
		return self.partial_update(request, *args, **kwargs)


class AppointmentCustomerListRetrieveAPIView(generics.ListAPIView):
	serializer_class = AppointmentCustomerRetrieveSerializer
	queryset = Appointment.objects.all()

	def get_queryset(self):
		return self.queryset.filter(customer__uid=self.kwargs['uid'])




class AppointmentCustomerRetrieve(generics.RetrieveAPIView):
	serializer_class = AppointmentCustomerRetrieveSerializer
	queryset = Appointment.objects.all()


