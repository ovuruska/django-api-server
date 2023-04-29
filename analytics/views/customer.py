from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveAPIView

from analytics.selectors import customer


@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class GetCustomerInvoiceDistributionView(RetrieveAPIView):

	@swagger_auto_schema(operation_description="Get customer invoice distribution", responses={
		200: openapi.Response(description="Customer invoice distribution",
			examples={"application/json": {"we_wash": 0.25, "grooming": 0.25, "tips": 0.25, "products": 0.25}})})
	def get(self, request, *args, **kwargs):
		customer_id = self.kwargs.get("pk")
		invoice_distribution = customer.get_customer_invoice_distribution(customer_id)
		return JsonResponse(invoice_distribution)


@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class GetAppointmentTypeCountDistributionView(RetrieveAPIView):
	@swagger_auto_schema(operation_description="Get customer appointment type count distribution", responses={
		200: openapi.Response(description="Customer appointment type count distribution",
			examples={"application/json": {"we_wash": 25, "grooming": 50}})})
	def get(self, request, *args, **kwargs):
		# /api/analytics/customer/appointment_types/<pk>
		customer_id = self.kwargs.get("pk")
		appointment_type_count_distribution = customer.get_appointment_type_count_distribution(customer_id)
		return JsonResponse(appointment_type_count_distribution)


@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class GetAppointmentCancellationRateView(RetrieveAPIView):
	@swagger_auto_schema(operation_description="Get customer cancellation rate", responses={
		200: openapi.Response(description="Percentage of appointments that were cancelled",
			examples={"application/json": {"rate": 25}})})
	def get(self, request, *args, **kwargs):
		customer_id = self.kwargs.get("pk")
		appointment_cancellation_rate = customer.get_appointment_cancellation_rate(customer_id)
		return JsonResponse({'rate': appointment_cancellation_rate * 100})


@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class GetAppointmentNoShowRateView(RetrieveAPIView):
	@swagger_auto_schema(operation_description="Get customer no show rate", responses={
		200: openapi.Response(description="Percentage of appointments that were no shows",
			examples={"application/json": {"rate": 35}})})
	def get(self, request, *args, **kwargs):
		customer_id = self.kwargs.get("pk")
		appointment_no_show_rate = customer.get_appointment_no_show_rate(customer_id)

		return JsonResponse({'rate': appointment_no_show_rate * 100})


@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class GetYearlyAppointmentSummaryView(RetrieveAPIView):
	@swagger_auto_schema(operation_description="Get customer no show rate", responses={
		200: openapi.Response(description="Percentage of appointments that were no shows", examples={
			"application/json": {"01-05-2022": {"tip": 10, "we_wash": 50, "grooming": 80, "products": 20},
				"01-06-2022": {"tip": 5, "we_wash": 40, "grooming": 70, "products": 15},
				"01-07-2022": {"tip": 0, "we_wash": 0, "grooming": 0, "products": 0},
				"01-08-2022": {"tip": 20, "we_wash": 60, "grooming": 100, "products": 25},
				"01-09-2022": {"tip": 0, "we_wash": 0, "grooming": 0, "products": 0},
				"01-10-2022": {"tip": 15, "we_wash": 30, "grooming": 60, "products": 10},
				"01-11-2022": {"tip": 0, "we_wash": 0, "grooming": 0, "products": 0},
				"01-12-2022": {"tip": 25, "we_wash": 40, "grooming": 120, "products": 30},
				"01-01-2023": {"tip": 0, "we_wash": 0, "grooming": 0, "products": 0},
				"01-02-2023": {"tip": 10, "we_wash": 20, "grooming": 50, "products": 5},
				"01-03-2023": {"tip": 0, "we_wash": 0, "grooming": 0, "products": 0},
				"01-04-2023": {"tip": 30, "we_wash": 70, "grooming": 140, "products": 35}}})})
	def get(self, request, *args, **kwargs):
		customer_id = self.kwargs.get("pk")
		response = customer.get_yearly_appointment_summary(customer_id)
		return JsonResponse(response)
