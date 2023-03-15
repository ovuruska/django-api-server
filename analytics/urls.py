from django.urls import path
from django.views.decorators.cache import cache_page

from analytics.views.customer import GetCustomerInvoiceDistributionView, GetAppointmentTypeCountDistributionView, \
	GetAppointmentCancellationRateView, GetAppointmentNoShowRateView, GetYearlyAppointmentSummaryView


urlpatterns = [
	path('customer/invoice_dist/<pk>', GetCustomerInvoiceDistributionView.as_view()),
	path('customer/visits/<pk>',GetAppointmentTypeCountDistributionView.as_view()),
	path('customer/cancellation_rate/<pk>', GetAppointmentCancellationRateView.as_view()),
	path('customer/no_show_rate/<pk>', GetAppointmentNoShowRateView.as_view()),
	path('customer/yearly_appointment_summary/<pk>', GetYearlyAppointmentSummaryView.as_view()),
]