from rest_framework import generics

from common.pagination import pagination
from transactions.models.transaction import Transaction
from transactions.serializers.transaction import TransactionSerializer


class GetTransactionsAPIView(generics.ListAPIView):
	serializer_class = TransactionSerializer

	def get_queryset(self):
		queryset = Transaction.objects.all()
		queryset = pagination(self.request, queryset)
		return queryset


class GetAppointmentTransactions(generics.ListAPIView):
	serializer_class = TransactionSerializer

	def get_queryset(self):
		pk = self.kwargs.get("pk")
		return Transaction.objects.filter(appointment_id=pk)
