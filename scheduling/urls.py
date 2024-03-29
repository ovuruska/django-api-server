from django.urls import path

import scheduling.views.branch
from . import views
from .views import LoginAPIView

products = [
	path('product/<int:pk>', views.ProductModifyAPIView.as_view(), name="product_modify"),
	path('product', views.ProductCreateAPIView.as_view(), name="product_retrieve"),
	path('products/all', views.ProductListAllAPIView.as_view(), name="product_list_all"),
]

branch_employees = [
	path('branch/<int:pk>/employees', views.BranchEmployeesAPIView.as_view(), name="branch_employees"),
	path('schedule/slots', views.EmployeeFreeTimesAPIView.as_view(), name="employee_free_times"),
	path('branch/<int:pk>/daily', views.BranchDailyInformationAPIView.as_view(), name="branch_daily_information"),
	path('branches/available', views.BranchAvailableEmployees.as_view(), name="branch_available_employees"),
]

services = [
	path('service/<int:pk>', views.ServiceModifyAPIView.as_view(), name="service_modify"),
	path('service', views.ServiceCreateAPIView.as_view(), name="service_retrieve"),
	path('services/all', views.ServiceListAllAPIView.as_view(), name="service_list_all"),
]

dogs = [
	path('dog', views.PetCreateAPIView.as_view(), name="dog_crud"),
	path('dog/<int:pk>', views.PetModifyRetrieveDestroyAPIView.as_view(), name="dog_retrieve"),
	path('pets', views.PetFilterView.as_view(), name="dog_filter"),
]


scheduling_appointments = [
	path('schedule/appointment/<int:pk>', views.AppointmentModifyAPIView.as_view(), name='appointment'),
	path('schedule/appointments/<int:pk>', views.AppointmentEmployeeRetrieveAPIView.as_view(), name='appointment'),
	path('customer/appointments', views.CustomerGetAppointmentsAPIView.as_view(), name='customer-appointments'),
	path('schedule/appointments', views.AppointmentFilterListViewV2_1.as_view(), name='appointment_filter_and_list'),
	path('v2/schedule/appointments', views.AppointmentFilterListViewV2_1.as_view(), name='appointment_filter_and_list'),
	path('schedule/appointment', views.AppointmentEmployeeCreateAPIView.as_view(),
	     name='scheduling/appointment-employee-create'),
]

auth = [
	# path('authorization/', include('knox.urls')),
	path('authorization/register', views.RegisterAPIView.as_view(), name='register'),
	path('authorization/login/', LoginAPIView.as_view()),

]


branch_working_hour = [
	path('scheduling/hours/branch/<int:pk>', views.BranchWorkingHourView.as_view(), name='scheduling-hours-create'),
]

employee_working_hour = [
	path('scheduling/hours/employee/<int:pk>', views.EmployeeWorkingHourRetrieveAPIView.as_view(),
	     name='scheduling-hours-list'),
]

employees = [
	path('employee', views.EmployeeCreateAPIView.as_view(), name='employee_create'),
	path('employee/groomers', views.EmployeeGroomerListRetrieve.as_view(), name='groomers_retrieve'),
	path('employee/<int:pk>', views.EmployeeRetrieveModifyDestroyAPIView.as_view(), name='employee_modify'),
	path('employees', views.EmployeeFilterView.as_view(), name='employee_filter'),
]

payrolls = [
	path('payrolls', views.PayrollListRetrieveView.as_view(), name='payroll_list'),
]

customers = [
	path('scheduling/customer/<int:pk>', views.CustomerDetailsAPIView.as_view(), name="customer_modify"),
	path('scheduling/customers', views.CustomerListView.as_view(), name="customer_list"),
	path('v2/scheduling/customers', views.CustomerFilterAPIView2.as_view(), name="customer_filter_v2"),
	path('me', views.GetCustomerFromTokenAPIView.as_view(), name="get-customer-from-token"),
	path('scheduling/customer/<int:pk>/pets', views.CustomerPetsListAPIView.as_view(), name="get_customer_dogs"),
]

branches = [
	path('branch', views.BranchCreateAPIView.as_view(), name='branch_create'),
]

urlpatterns = [
	path('branches/all', views.BranchListAllAPIView.as_view(), name="branch_list_all"),
	path('branch/<pk>', scheduling.views.branch.BranchRetrieveModifyAPIView.as_view(), name="admin_branch_modify"),
]

signed_url = [
	path('confirmation/<token>/approve', views.SignedUrlApproveAPIView.as_view(), name='signed_url_approve'),
	path('confirmation/<token>/cancel', views.SignedUrlCancelAPIView.as_view(), name='signed_url_cancel'),
	path('confirmation/<token>/reschedule', views.SignedUrlRescheduleAPIView.as_view(), name='signed_url_reschedule'),
]

urlpatterns = urlpatterns + branch_working_hour + products + services + dogs +  employees \
              + employee_working_hour + scheduling_appointments + payrolls + signed_url + branches + customers + auth + branch_employees
