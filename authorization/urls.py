from django.urls import path

from authorization import views
from authorization.views import CustomerVerifyTokenView


urlpatterns = [
	path("employee/login", views.EmployeeLoginAPIView.as_view(), name="authorization/employee-login"),
	path("customer/login", views.CustomerLoginAPIView.as_view(), name="authorization/customer-login"),

	path("customer/register", views.CustomerRegisterAPIView.as_view(), name="authorization/customer-register"),
	path('customer/verify', CustomerVerifyTokenView.as_view(), name='authorization/verify-token'),


]