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
]
