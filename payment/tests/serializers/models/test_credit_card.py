"""
from rest_framework.serializers import ModelSerializer

from payment.models.credit_card import CreditCard

class CreditCardSerializer(ModelSerializer):
	class Meta:
		model = CreditCard
		fields = ('id', 'exp_month', 'exp_year', 'first6', 'last4', 'brand', 'created_at', 'updated_at')
"""

from django.test import TestCase

from payment.serializers.models.credit_card import CreditCardSerializer


class CreditCardSerializerTestCase(TestCase):
	base = {
		"exp_month": "12",
		"exp_year": "2025",
		"first6": "123456",
		"last4": "1234",
		"brand": "Visa",
		"created_at": "2020-12-12T12:12:12Z",
		"updated_at": "2020-12-12T12:12:12Z"
	}

	def test_valid(self):
		serializer = CreditCardSerializer(data=self.base)
		self.assertTrue(serializer.is_valid())

	def test_invalid(self):
		serializer = CreditCardSerializer(data={})
		self.assertFalse(serializer.is_valid())

