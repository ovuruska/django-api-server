from django.urls import path

from . import views

urlpatterns = [
    path('transactions', views.GetTransactionsAPIView.as_view(), name='get_transactions'),
	path('transaction/<int:pk>', views.GetAppointmentTransactions.as_view(), name='get_transaction')
]
