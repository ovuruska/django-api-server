from django.test import TestCase

from authorization.serializers.requests.login_customer import LoginCustomerRequestSerializer


class LoginCustomerRequestSerializerTestCase( TestCase ):


	def test_valid(self):
		data = {
			'email': 'a@a.com',
			'password': 'password'
		}
		serializer = LoginCustomerRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		validated_data = serializer.validated_data

	def test_invalid_email(self):
		data = {
			'email': 'a',
			'password': 'password'
		}
		serializer = LoginCustomerRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_invalid_missing_field(self):
		data = {
			'email': ''
		}
		serializer = LoginCustomerRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

