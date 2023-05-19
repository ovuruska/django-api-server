from datetime import datetime

from rest_framework import serializers
import re

class AddressSerializer(serializers.Serializer):
	city = serializers.CharField()
	country = serializers.CharField()
	address_line_1 = serializers.CharField()
	address_line_2 = serializers.CharField()
	postal_code = serializers.CharField()
	state = serializers.CharField()

class CreateCreditCardRequestSerializer(serializers.Serializer):
	address = AddressSerializer()
	card_number = serializers.CharField()
	cvv = serializers.CharField()
	exp_date = serializers.CharField()
	brand = serializers.CharField()
	cardholder_name = serializers.CharField()

	def validate(self,data):
		cvv = data.get('cvv')
		card_number = data.get('card_number')
		exp_date = data.get('exp_date')
		if not cvv.isdigit():
			raise serializers.ValidationError("CVV must be numeric.")
		if len(cvv) != 3:
			raise serializers.ValidationError("CVV must be 3 digits long.")

		if not re.match(r'(0[1-9]|1[0-2])\/?([0-9]{2,4})$', exp_date):
			raise serializers.ValidationError("Expiration date must be in the format 'MM/YY'.")

		# Validate if the date is in the future
		current_date = datetime.now()
		current_date = datetime.strftime(current_date, '%m/%y')
		if exp_date <= current_date:
			raise serializers.ValidationError("Expiration date must be in the future.")

		card_number = re.sub(r'\s', '', card_number)
		if not card_number.isdigit():
			raise serializers.ValidationError("Credit card number must be numeric.")

		if len(card_number) != 16:
			raise serializers.ValidationError("Credit card number must be 16 digits long.")

		return data