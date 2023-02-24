from django.urls import path

from . import views

urlpatterns = [
    path('transactions', views.GetTransactionsAPIView, name='get_transactions')
]
