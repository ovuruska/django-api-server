from django.urls import path

from . import views

urlpatterns = [
    path('transactions', views.GetTransactionsAPIView.as_view(), name='get_transactions')
]
