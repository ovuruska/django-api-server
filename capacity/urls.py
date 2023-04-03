from django.urls import path

from capacity.views.daily_capacity import GetDailyCapacityView
from capacity.views.monthly_capacity import GetMonthlyCapacityView

urlpatterns = [
	path('monthly', GetMonthlyCapacityView.as_view(), name='get_monthly_capacity'),
	path('daily', GetDailyCapacityView.as_view(), name='capacity/get_daily_capacity')
]