from rest_framework.serializers import ModelSerializer

from payment.models.credit_card import CreditCard

class CreditCardSerializer(ModelSerializer):
	class Meta:
		model = CreditCard
		fields = ('id', 'exp_month', 'exp_year', 'first6', 'last4', 'brand', 'created_at', 'updated_at')