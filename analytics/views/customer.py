from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import RetrieveAPIView

from analytics.selectors import customer


@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class GetCustomerInvoiceDistributionView(RetrieveAPIView):

	def get(self, request, *args, **kwargs):
		# /api/analytics/customer/invoice_distribution/<pk>
		customer_id = self.kwargs.get("pk")
		invoice_distribution = customer.get_customer_invoice_distribution(customer_id)
		return JsonResponse(invoice_distribution)


@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class GetAppointmentTypeCountDistributionView(RetrieveAPIView):

	def get(self, request, *args, **kwargs):
		# /api/analytics/customer/appointment_types/<pk>
		customer_id = self.kwargs.get("pk")
		appointment_type_count_distribution = customer.get_appointment_type_count_distribution(customer_id)
		return JsonResponse(appointment_type_count_distribution)


@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class GetAppointmentCancellationRateView(RetrieveAPIView):

	def get(self, request, *args, **kwargs):
		customer_id = self.kwargs.get("pk")
		appointment_cancellation_rate = customer.get_appointment_cancellation_rate(customer_id)
		return JsonResponse({
			'rate': appointment_cancellation_rate * 100
		})


@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class GetAppointmentNoShowRateView(RetrieveAPIView):

	def get(self, request, *args, **kwargs):
		customer_id = self.kwargs.get("pk")
		appointment_no_show_rate = customer.get_appointment_no_show_rate(customer_id)

		return JsonResponse({
			'rate': appointment_no_show_rate * 100
		})


@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class GetYearlyAppointmentSummaryView(RetrieveAPIView):

	def get(self, request, *args, **kwargs):
		customer_id = self.kwargs.get("pk")
		response = customer.get_yearly_appointment_summary(customer_id)
		return JsonResponse(response)
