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
]