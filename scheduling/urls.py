from django.urls import path

from . import views

urlpatterns = [
	path('appointment/create', views.AppointmentCreateAPIView.as_view(), name='appointment'),
	path('branch/<pk>', views.BranchRetrieveAPIView.as_view(), name='branch_list'),
	path('admin/branch/',views.BranchModifyAPIView.as_view(),name="admin_branch_modify"),
	path('me/<uid>',views.CustomerRetrieveAPIView.as_view(),name="get_customer_details")
]
