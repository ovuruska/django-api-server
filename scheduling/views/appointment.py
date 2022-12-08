from datetime import datetime
from datetime import timedelta

from rest_framework import generics

from ..models import Customer, Service
from ..serializers.Appointment import *
from dateutil.parser import isoparse

class AppointmentCreateAPIView(generics.CreateAPIView):
	"""

	start_time: Datetime String in ISO 8601 format : https://www.iso.org/iso-8601-date-and-time-format.html
	"""

	serializer_class = AppointmentCreateSerializer
	queryset = Appointment.objects.all()

	def post(self, request, *args, **kwargs):
		customer = Customer.objects.get(uid=request.data["customer"])
		request.data["customer"] = customer.id
		total_duration = timedelta()
		for service in request.data["services"]:
			service_instance = Service.objects.get(id=service)
			total_duration += service_instance.duration
		start_time = isoparse(request.data["start_time"])
		request.data["start_time"] = start_time
		request.data["end_time"] = start_time + total_duration
		return super().create(request, *args, **kwargs)


class AppointmentModifyAPIView(generics.UpdateAPIView):
	serializer_class = AppointmentEmployeeSerializer
	queryset = Appointment.objects.all()


class AppointmentCustomerListRetrieveAPIView(generics.ListAPIView):
	serializer_class = AppointmentCustomerRetrieveSerializer
	queryset = Appointment.objects.all()

	def get(self, request, *args, **kwargs):
		self.queryset = self.queryset.filter(customer__uid=self.kwargs['uid'])
		return super().get(request, *args, **kwargs)


class AppointmentEmployeeRetrieveAPIView(generics.RetrieveAPIView):
	serializer_class = AppointmentEmployeeSerializer
	queryset = Appointment.objects.all()


class AppointmentCustomerRetrieve(generics.RetrieveAPIView):
	serializer_class = AppointmentCustomerRetrieveSerializer
	queryset = Appointment.objects.all()
