from django.urls import path
from . import views

products = [
	path('product/<pk>', views.ProductModifyAPIView.as_view(), name="product_modify"),
	path('product', views.ProductCreateAPIView.as_view(), name="product_retrieve"),
	path('products/all', views.ProductListAllAPIView.as_view(), name="product_list_all"),
]

services = [
	path('service/<pk>', views.ServiceModifyAPIView.as_view(), name="service_modify"),
	path('service', views.ServiceCreateAPIView.as_view(), name="service_retrieve"),
	path('services/all', views.ServiceListAllAPIView.as_view(), name="service_list_all"),
]

dogs = [
	path('dog', views.DogCreateAPIView.as_view(), name="dog_crud"),
	path('dog/<pk>', views.DogModifyRetrieveDestroyAPIView.as_view(), name="dog_retrieve"),
	path('dogs/<uid>', views.CustomerDogsRetrieveAPIView.as_view(), name="get_customer_dogs"),
]

appointments = [
	path('appointment', views.AppointmentCreateAPIView.as_view(), name='appointment'),
	path('appointment/<pk>', views.AppointmentCustomerRetrieve.as_view(), name='appointment_modify'),
	path('appointments/<uid>', views.AppointmentCustomerListRetrieveAPIView.as_view(), name='appointment_list'),
]

scheduling_appointments = [
	path('schedule/appointment/<pk>', views.AppointmentModifyAPIView.as_view(), name='appointment'),
	path('schedule/appointments',views.AppointmentFilterListView.as_view(), name='appointment_filter_and_list'),
]



employees = [
	path('employee', views.EmployeeCreateAPIView.as_view(), name='employee_create'),
	path('employee/groomers', views.EmployeeGroomerListRetrieve.as_view(), name='groomers_retrieve'),
	path('employee/<pk>', views.EmployeeRetrieveModifyDestroyAPIView.as_view(), name='employee_modify'),

]

payrolls = [
	path('payrolls', views.PayrollListRetrieveView.as_view(), name='payroll_list'),
]


urlpatterns = [
	path('branch/<pk>', views.BranchRetrieveAPIView.as_view(), name='branch_list'),
	path('admin/branch/',views.BranchModifyAPIView.as_view(),name="admin_branch_modify"),
	path('me/<uid>',views.CustomerRetrieveAPIView.as_view(),name="get_customer_details"),
]

urlpatterns = urlpatterns + products + services + dogs + appointments + employees + scheduling_appointments + payrolls
