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
	path('dog', views.DogModifyAPIView.as_view(), name="dog_crud"),
	path('dog/<pk>', views.DogRetrieveAPIView.as_view(), name="dog_retrieve"),
	path('dogs/<uid>', views.CustomerDogsRetrieveAPIView.as_view(), name="get_customer_dogs"),
]

appointments = [
	path('appointment', views.AppointmentCreateAPIView.as_view(), name='appointment'),
	path('appointment/<pk>', views.AppointmentCustomerRetrieve.as_view(), name='appointment_modify'),
	path('appointments/<uid>', views.AppointmentCustomerListRetrieveAPIView.as_view(), name='appointment_list'),
	path('admin/appointment/<pk>', views.AppointmentEmployeeRetrieveAPIView.as_view(), name='appointment_employee_retrieve'),
	path('admin/appointment', views.AppointmentModifyAPIView.as_view(), name='appointment_employee_modify'),
]

urlpatterns = [
	path('branch/<pk>', views.BranchRetrieveAPIView.as_view(), name='branch_list'),
	path('admin/branch/',views.BranchModifyAPIView.as_view(),name="admin_branch_modify"),
	path('me/<uid>',views.CustomerRetrieveAPIView.as_view(),name="get_customer_details"),
]

urlpatterns = urlpatterns + products + services + dogs + appointments
