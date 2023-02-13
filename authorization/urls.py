from django.urls import path

from authorization import views

"""
urlpatterns = [
	path("customer/login"),
	path("customer/register"),
	path("customer/logout"),
	path("employee/login"),
]
"""
urlpatterns = [
	path("employee/login", views.EmployeeLoginAPIView.as_view(), name="employee_login"),
	path("customer/login", views.CustomerLoginAPIView.as_view(), name="customer_login"),
	path("customer/register", views.CustomerRegisterAPIView.as_view(), name="customer_register"),
]