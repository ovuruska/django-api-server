from django.urls import path

from authorization import views
from authorization.views import VerifyTokenView


urlpatterns = [
	path("employee/login", views.EmployeeLoginAPIView.as_view(), name="employee_login"),
	path("customer/login", views.CustomerLoginAPIView.as_view(), name="customer_login"),
	path("customer/register", views.CustomerRegisterAPIView.as_view(), name="authorization/customer-register"),
	path('customer/verify', VerifyTokenView.as_view(), name='authorization/verify-token'),

]