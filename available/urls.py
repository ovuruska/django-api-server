from django.urls import path

from available.views.daily_view import DailyAvailableView

urlpatterns = [
	path('daily', DailyAvailableView.as_view(), name='available/daily_available'),
]