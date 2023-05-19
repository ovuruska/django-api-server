from django.test import TestCase

from payment.serializers.requests.create_credit_card import CreateCreditCardRequestSerializer


class CreateCreditCardSerializerTestCase(TestCase):
	base = {
		"address": {
			"city": "string",
			"country": "string",
			"address_line_1": "string",
			"address_line_2": "string",
			"postal_code": "string",
			"state": "string"

		},
		"card_number": "string",
		"cvv": "string",
		"exp_date": "string",
		"brand": "string",
		"cardholder_name": "string"

	}

	def test_invalid(self):
		serializer = CreateCreditCardRequestSerializer(data=self.base)
		self.assertFalse(serializer.is_valid())

	def test_valid(self):
		data = {
			**self.base,
			"card_number": "1234123412341234",
			"cvv": "123",
			"exp_date": "12/2020",
		}
		serializer = CreateCreditCardRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())

	def test_invalid_cvv(self):
		data = {
			**self.base,
			"card_number": "1234123412341234",
			"cvv": "1234",
		}
		serializer = CreateCreditCardRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_invalid_card_number(self):
		data = {
			**self.base,
			"cvv": "123",
			"card_number": "123412341234123412341234",
		}
		serializer = CreateCreditCardRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_invalid_exp_date(self):
		data = {
			**self.base,
			"cvv": "123",
			"card_number": "1234123412341234",
			"exp_date": "12/20",
		}
		serializer = CreateCreditCardRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())


	def test_check_address_fields_are_serialized_correctly(self):
		data ={
			**self.base,
			"card_number": "1234123412341234",
			"cvv": "123",
			"exp_date": "12/2020",
		}
		serializer = CreateCreditCardRequestSerializer(data=data)
		serializer.is_valid()
		self.assertEqual(serializer.data['address']['city'], data['address']['city'])
		self.assertEqual(serializer.data['address']['country'], data['address']['country'])
		self.assertEqual(serializer.data['address']['address_line_1'], data['address']['address_line_1'])
		self.assertEqual(serializer.data['address']['address_line_2'], data['address']['address_line_2'])
		self.assertEqual(serializer.data['address']['postal_code'], data['address']['postal_code'])
		self.assertEqual(serializer.data['address']['state'], data['address']['state'])
