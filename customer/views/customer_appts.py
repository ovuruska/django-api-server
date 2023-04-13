from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from customer.selectors.appts import get_customer_past_appts, get_customer_upcoming_appts, get_customer_all_appts
from customer.serializers.responses.appt_response import CustomerAppointmentResponseSerializer


class BaseCustomerAppointmentAPIView(generics.ListAPIView):
	serializer_class = CustomerAppointmentResponseSerializer
	pagination_class = LimitOffsetPagination

	def paginate_queryset(self, queryset):
		if self.paginator is None:
			return None
		return self.paginator.paginate_queryset(queryset, self.request, view=self)

	def get_paginated_response(self, data):
		assert self.paginator is not None
		return self.paginator.get_paginated_response(data)

	def get(self, request, *args, **kwargs):
		all_queryset = self.get_queryset()
		queryset = self.filter_queryset(all_queryset)
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		else:

			return Response({
				"count":all_queryset.count(),
				"results":[],
				"next":None,
				"previous":None
			})



class GetCustomerPastAppts(BaseCustomerAppointmentAPIView):

	def get_queryset(self):
		customer = self.request.user.customer
		return get_customer_past_appts(customer)


class GetCustomerUpcomingAppts(BaseCustomerAppointmentAPIView):

	def get_queryset(self):
		customer = self.request.user.customer
		return get_customer_upcoming_appts(customer)


class GetCustomerAllAppts(BaseCustomerAppointmentAPIView):
	def get_queryset(self):
		customer = self.request.user.customer
		return get_customer_all_appts(customer)
