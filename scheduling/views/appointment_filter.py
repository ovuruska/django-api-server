from django.contrib.auth.mixins import PermissionRequiredMixin
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from common.pagination import pagination
from common.permissions.view_all_appointments import CanViewAllAppointments
from common.search_pagination import SearchPagination
from scheduling.models import Appointment, Branch
from scheduling.serializers.Appointment import AppointmentEmployeeSerializer


class AppointmentFilterListView(generics.ListAPIView, PermissionRequiredMixin):
	permission_classes = [CanViewAllAppointments]
	serializer_class = AppointmentEmployeeSerializer
	filter_backends = (DjangoFilterBackend,)

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	def get_queryset(self):
		ordering = self.request.query_params.get('ordering', '-start')
		queryset = Appointment.objects.order_by(ordering).all()
		start_date = self.request.query_params.get('start__gt', None)
		if start_date is not None:
			queryset = queryset.filter(start__gt=start_date)

		end_date = self.request.query_params.get('start__lt', None)
		if end_date:
			queryset = queryset.filter(start__lt=end_date)

		status = self.request.query_params.get('status', None)
		if status:
			queryset = queryset.filter(status=status)

		employee_id = self.request.query_params.get('employee', None)
		if employee_id:
			queryset = queryset.filter(employee=employee_id)

		customer_id = self.request.query_params.get('customer', None)
		if customer_id:
			queryset = queryset.filter(customer__id=customer_id)

		dog_id = self.request.query_params.get('pet', None)
		if dog_id:
			queryset = queryset.filter(dog__id=dog_id)

		branch_id = self.request.query_params.get('branch',)
		if branch_id:
			queryset = queryset.filter(branch__id=branch_id)

		service = self.request.query_params.get('service', None)
		if service:
			queryset = queryset.filter(appointment_type=service)

		queryset = pagination(self.request,queryset)

		return queryset

class AppointmentFilterListViewV2(AppointmentFilterListView):
	pagination_class = SearchPagination


class AppointmentFilterListViewV2_1(AppointmentFilterListView):
	pagination_class = LimitOffsetPagination

	@swagger_auto_schema(manual_parameters=[
		openapi.Parameter('start__gt', openapi.IN_QUERY, description="Start date greater than", type=openapi.TYPE_STRING),
		openapi.Parameter('start__lt', openapi.IN_QUERY, description="Start date less than", type=openapi.TYPE_STRING),
		openapi.Parameter('employee', openapi.IN_QUERY, description="Employee id", type=openapi.TYPE_INTEGER),
		openapi.Parameter('customer', openapi.IN_QUERY, description="Customer id", type=openapi.TYPE_INTEGER),
		openapi.Parameter('pet', openapi.IN_QUERY, description="Pet Id", type=openapi.TYPE_INTEGER),
		openapi.Parameter('branch', openapi.IN_QUERY, description="Branch id", type=openapi.TYPE_INTEGER),
		openapi.Parameter('limit', openapi.IN_QUERY, description="Limit", type=openapi.TYPE_INTEGER,default=50),
		openapi.Parameter('offset', openapi.IN_QUERY, description="Offset", type=openapi.TYPE_INTEGER,default=0),
		openapi.Parameter('ordering', openapi.IN_QUERY, description="Ordering", type=openapi.TYPE_STRING,default='-start'),
		openapi.Parameter('status', openapi.IN_QUERY, description="Status", type=openapi.TYPE_STRING),
	])
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)


