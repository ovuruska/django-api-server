from django.urls import path

urlpatterns = [
	path('/capacity/monthly', GetMonthlyCapacity.as_view()),
]