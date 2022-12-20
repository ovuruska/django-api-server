from datetime import timedelta

from dateutil.parser import isoparse
from rest_framework import generics
from rest_framework.response import Response

from ..models import Customer, Service, Dog
from ..serializers.Appointment import *


class AppointmentCreateAPIView(generics.CreateAPIView):
	"""

	start: Datetime String in ISO 8601 format : https://www.iso.org/iso-8601-date-and-time-format.html
	"""

	serializer_class = AppointmentCreateSerializer
	queryset = Appointment.objects.all()

	def post(self, request, *args, **kwargs):
		customer = Customer.objects.get(uid=request.data["customer"])
		request.data["customer"] = customer.id
		dog_data = request.data["dog"]
		if type(dog_data) == int:
			request.data["dog"] = dog_data
		else:
			dog, _ = Dog.objects.get_or_create(
				owner=customer,
				name=dog_data,
			)
			request.data["dog"] = dog.id

		branch_id = request.data["branch"]

		total_duration = timedelta()
		for service in request.data["services"]:
			service_instance = Service.objects.get(id=service)
			total_duration += service_instance.duration
		start = isoparse(request.data["start"])
		request.data["start"] = start
		request.data["end"] = start + total_duration
		try:
			Appointment.objects.get(
				branch=branch_id,
				start__gte=request.data["start"],
				end__lte=request.data["end"]
			)
			return Response({"error": "There is already an appointment at this time"}, status=400,
			                content_type="application/json")

		except Appointment.DoesNotExist:

			return self.create(request, *args, **kwargs)


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


