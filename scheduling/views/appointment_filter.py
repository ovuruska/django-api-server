from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.pagination import pagination
from common.permissions.view_all_appointments import CanViewAllAppointments
from common.search_pagination import SearchPagination
from scheduling.models import Appointment, Branch
from scheduling.selectors.branch import get_free_hours
from scheduling.serializers.Appointment import AppointmentEmployeeSerializer
from scheduling.serializers.Branch import FreeHoursSerializer


class AppointmentFilterListView(generics.ListAPIView, PermissionRequiredMixin):
	permission_classes = [CanViewAllAppointments]
	serializer_class = AppointmentEmployeeSerializer
	filter_backends = (DjangoFilterBackend,)

	filterset_fields = ["start", "branch", "status", "employee", "dog"]

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	def get_queryset(self):
		queryset = Appointment.objects.order_by('-start').all()
		start_date = self.request.query_params.get('start__gt', None)
		if start_date is not None:
			queryset = queryset.filter(start__gt=start_date)

		end_date = self.request.query_params.get('start__lt', None)
		if end_date:
			queryset = queryset.filter(start__lt=end_date)

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
		openapi.Parameter('limit', openapi.IN_QUERY, description="Limit", type=openapi.TYPE_INTEGER),
		openapi.Parameter('offset', openapi.IN_QUERY, description="Offset", type=openapi.TYPE_INTEGER),
	])
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)


