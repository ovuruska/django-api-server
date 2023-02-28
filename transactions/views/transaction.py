from rest_framework import generics

from transactions.models.transaction import Transaction
from transactions.serializers.transaction import TransactionSerializer


class GetTransactionsAPIView(generics.ListAPIView):
	serializer_class = TransactionSerializer
	queryset = Transaction.objects.all()


class GetAppointmentTransactions(generics.ListAPIView):
	serializer_class = TransactionSerializer

	def get_queryset(self):
		pk = self.kwargs.get("pk")
		return Transaction.objects.filter(appointment_id=pk)
