from django.urls import path

from . import views

urlpatterns = [
	path('appointment/create', views.AppointmentCreateAPIView.as_view(), name='appointment'),
	path('branch/<pk>', views.BranchRetrieveAPIView.as_view(), name='branch_list'),
]
