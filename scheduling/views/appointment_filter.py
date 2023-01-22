from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from scheduling.models import Appointment, Branch
from scheduling.selectors.branch import get_free_hours
from scheduling.serializers.Appointment import AppointmentEmployeeSerializer
from scheduling.serializers.Branch import FreeHoursSerializer


class AppointmentFilterListView(generics.ListAPIView):
	serializer_class = AppointmentEmployeeSerializer
	filter_backends = (DjangoFilterBackend,)
	# permission_classes = [IsAuthenticated]

	filterset_fields = ["start","branch","status"]

	def get_queryset(self):
		queryset = Appointment.objects.all()
		start_date = self.request.query_params.get('start__gt', None)
		if start_date is not None:
			queryset = queryset.filter(start__gt=start_date)

		end_date = self.request.query_params.get('start__lt', None)
		if end_date:
			queryset = queryset.filter(start__lt=end_date)
		return queryset



class AppointmentAvailableHoursView(generics.RetrieveAPIView):

	queryset = Appointment.objects.all()
	serializer_class = FreeHoursSerializer

	def get(self, request, *args, **kwargs):
		branch_id = self.kwargs.get("pk")
		# Check if branch exists
		_ = Branch.objects.get(id=branch_id)

		date = request.GET.get("date")
		free_hours = get_free_hours(branch_id, date)
		return Response(
			data={
				"free_hours": free_hours
			},
			status=200,
			headers={
				"Content-Type": "application/json"
			}
		)



