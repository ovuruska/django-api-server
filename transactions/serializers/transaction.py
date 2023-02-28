from rest_framework import serializers

from scheduling.models import Employee
from transactions.models.transaction import Transaction


class TransactionEmployeeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Employee
		fields = ["id", "name"]


class TransactionSerializer(serializers.ModelSerializer):
	employee = TransactionEmployeeSerializer(read_only=True)

	class Meta:
		model = Transaction
		fields = '__all__'
