from rest_framework import generics

from transactions.models.transaction import Transaction
from transactions.serializers.transaction import TransactionSerializer


class GetTransactionsAPIView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()