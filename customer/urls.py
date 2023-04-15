from django.urls import path

from customer.views.appointment import CustomerCreateAppointment
from customer.views.customer_appts import GetCustomerPastAppts, GetCustomerUpcomingAppts, GetCustomerAllAppts
from customer.views.pet_details import GetCustomerPetDetails

urlpatterns = [
	path("appointments/past", GetCustomerPastAppts.as_view(), name="customer/appointments/past"),
	path("appointments/upcoming", GetCustomerUpcomingAppts.as_view(), name="customer/appointments/upcoming"),
	path("appointments/all", GetCustomerAllAppts.as_view(), name="customer/appointments/all"),
	path("pets/all", GetCustomerPetDetails.as_view(), name="customer/pets/all"),
	path('appointment/create', CustomerCreateAppointment.as_view(), name="customer/appointment/create"),
]