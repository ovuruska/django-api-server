from rest_framework import serializers

from scheduling.models import Payroll


class PayrollSerializer(serializers.ModelSerializer):

	class Meta:
		model = Payroll
		fields = "__all__"