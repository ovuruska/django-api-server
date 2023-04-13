from django.urls import path

from customer.views.customer_appts import GetCustomerPastAppts, GetCustomerUpcomingAppts, GetCustomerAllAppts

urlpatterns = [
	path("appointments/past", GetCustomerPastAppts.as_view(), name="customer/appointments/past"),
	path("appointments/upcoming", GetCustomerUpcomingAppts.as_view(), name="customer/appointments/upcoming"),
	path("appointments/all", GetCustomerAllAppts.as_view(), name="customer/appointments/all"),
]