from django.urls import path

from capacity.views.monthly_capacity import GetMonthlyCapacity

urlpatterns = [
	path('monthly', GetMonthlyCapacity.as_view(), name='get_monthly_capacity'),
]