from django.urls import path

import scheduling.views.branch
from . import views
from .views import LoginAPIView

products = [
	path('product/<pk>', views.ProductModifyAPIView.as_view(), name="product_modify"),
	path('product', views.ProductCreateAPIView.as_view(), name="product_retrieve"),
	path('products/all', views.ProductListAllAPIView.as_view(), name="product_list_all"),
]

branch_employees = [
	path('branch/<pk>/employees', views.BranchEmployeesAPIView.as_view(), name="branch_employees"),
	path('schedule/slots', views.EmployeeFreeTimesAPIView.as_view(), name="employee_free_times"),

]

services = [
	path('service/<pk>', views.ServiceModifyAPIView.as_view(), name="service_modify"),
	path('service', views.ServiceCreateAPIView.as_view(), name="service_retrieve"),
	path('services/all', views.ServiceListAllAPIView.as_view(), name="service_list_all"),
]

dogs = [
	path('dog', views.PetCreateAPIView.as_view(), name="dog_crud"),
	path('dog/<pk>', views.PetModifyRetrieveDestroyAPIView.as_view(), name="dog_retrieve"),
	path('pets', views.PetFilterView.as_view(), name="dog_filter"),
]

appointments = [
	path('appointment', views.AppointmentCreateAPIView.as_view(), name='appointment_create'),
	path('appointment/<pk>', views.AppointmentCustomerRetrieve.as_view(), name='appointment_modify'),
]

scheduling_appointments = [
	path('schedule/appointment/<pk>', views.AppointmentModifyAPIView.as_view(), name='appointment'),
	path('schedule/appointments/<pk>', views.AppointmentEmployeeRetrieveAPIView.as_view(), name='appointment'),
	path('customer/appointments', views.CustomerGetAppointmentsAPIView.as_view(), name='customer-appointments'),
	path('schedule/appointments', views.AppointmentFilterListView.as_view(), name='appointment_filter_and_list'),
	path('v2/schedule/appointments', views.AppointmentFilterListViewV2.as_view(),
	     name='appointment_filter_and_list_v2'),
	path('v2.1/schedule/appointments', views.AppointmentFilterListViewV2_1.as_view(),
	     name='appointment_filter_and_list_v2_1'),
	path('schedule/appointment', views.EmployeeCreateAppointmentView.as_view(),
	     name='appointment_employee_create_api_view'),
]

auth = [
	# path('authorization/', include('knox.urls')),
	path('authorization/register', views.RegisterAPIView.as_view(), name='register'),
	path('authorization/login/', LoginAPIView.as_view()),

]


branch_working_hour = [
	path('scheduling/hours/branch/<pk>', views.BranchWorkingHourView.as_view(), name='scheduling-hours-create'),
]

employee_working_hour = [
	path('scheduling/hours/employee', views.EmployeeWorkingHourCreateAPIView.as_view(), name='scheduling-hours-create'),
	path('scheduling/hours/employee/<pk>', views.EmployeeWorkingHourRetrieveAPIView.as_view(),
	     name='scheduling-hours-list'),
]

employees = [
	path('employee', views.EmployeeCreateAPIView.as_view(), name='employee_create'),
	path('employee/groomers', views.EmployeeGroomerListRetrieve.as_view(), name='groomers_retrieve'),
	path('employee/<pk>', views.EmployeeRetrieveModifyDestroyAPIView.as_view(), name='employee_modify'),
	path('employees', views.EmployeeFilterView.as_view(), name='employee_filter'),
]

payrolls = [
	path('payrolls', views.PayrollListRetrieveView.as_view(), name='payroll_list'),
]

customers = [
	path('scheduling/customer/<pk>', views.CustomerDetailsAPIView.as_view(), name="customer_modify"),
	path('scheduling/customers', views.CustomerFilterAPIView.as_view(), name="customer_filter"),
	path('v2/scheduling/customers', views.CustomerFilterAPIView2.as_view(), name="customer_filter_v2"),
	path('me', views.GetCustomerFromTokenAPIView.as_view(), name="get-customer-from-token"),
	path('scheduling/customer/<pk>/pets', views.CustomerPetsListAPIView.as_view(), name="get_customer_dogs"),
]

branches = [
	path('branch', views.BranchCreateAPIView.as_view(), name='branch_create'),
]

urlpatterns = [
	path('branch/<pk>', scheduling.views.branch.BranchRetrieveModifyAPIView.as_view(), name="admin_branch_modify"),
	path('branch/<pk>/free_hours', views.AppointmentAvailableHoursView.as_view(), name="get_available_hours")
]

signed_url = [
	path('confirmation/<token>/approve', views.SignedUrlApproveAPIView.as_view(), name='signed_url_approve'),
	path('confirmation/<token>/cancel', views.SignedUrlCancelAPIView.as_view(), name='signed_url_cancel'),
	path('confirmation/<token>/reschedule', views.SignedUrlRescheduleAPIView.as_view(), name='signed_url_reschedule'),
]

urlpatterns = urlpatterns + branch_working_hour + products + services + dogs + appointments + employees \
              + employee_working_hour + scheduling_appointments + payrolls + signed_url + branches + customers + auth + branch_employees
