from django.urls import path

from . import views

urlpatterns = [
	path('appointment/create', views.AppointmentCreateAPIView.as_view(), name='appointment'),
	path('branch/<pk>', views.BranchRetrieveAPIView.as_view(), name='branch_list'),
	path('admin/branch/',views.BranchModifyAPIView.as_view(),name="admin_branch_modify"),
	path('me/<uid>',views.CustomerRetrieveAPIView.as_view(),name="get_customer_details"),
	path('dog',views.DogModifyAPIView.as_view(),name="dog_crud"),
	path('dog/<pk>',views.DogRetrieveAPIView.as_view(),name="dog_retrieve"),
	path('dogs/<uid>',views.CustomerDogsRetrieveAPIView.as_view(),name="get_customer_dogs"),
	path('service/<pk>',views.ServiceModifyAPIView.as_view(),name="service_modify"),
	path('service',views.ServiceCreateAPIView.as_view(),name="service_retrieve"),
	path('services/all',views.ServiceListAllAPIView.as_view(),name="service_list_all"),
	path('product/<pk>',views.ProductModifyAPIView.as_view(),name="product_modify"),
	path('product',views.ProductCreateAPIView.as_view(),name="product_retrieve"),
	path('products/all',views.ProductListAllAPIView.as_view(),name="product_list_all"),
]
