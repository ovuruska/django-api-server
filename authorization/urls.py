from django.urls import path

from authorization import views
from authorization.views import VerifyTokenView


urlpatterns = [
	path("employee/login", views.EmployeeLoginAPIView.as_view(), name="authorization/employee-login"),
	path("customer/login", views.CustomerLoginAPIView.as_view(), name="authorization/customer-login"),
	path("customer/register", views.RegisterCustomerAPIView.as_view(), name="authorization/customer-register"),
	path('customer/verify', VerifyTokenView.as_view(), name='authorization/verify-token'),

]