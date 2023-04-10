from django.test import TestCase

from authorization.serializers.requests.register_customer import RegisterCustomerRequestSerializer


class RegisterCustomerRequestSerializerTestCase( TestCase ):
	def test_valid(self):
		data = {
			'email': 'email@email.com',
			'password': 'password',
			'first_name': 'first_name',
			'last_name': 'last_name'
		}
		serializer = RegisterCustomerRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		validated_data = serializer.validated_data
		self.assertEqual(validated_data['email'], data['email'])
		self.assertEqual(validated_data['password'], data['password'])
		self.assertEqual(validated_data['first_name'], data['first_name'])
		self.assertEqual(validated_data['last_name'], data['last_name'])

	def test_invalid_email(self):
		data = {
			'email': 'email',
			'password': 'password',
			'first_name': 'first_name',
			'last_name': 'last_name'
		}
		serializer = RegisterCustomerRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_invalid_missing_field(self):
		data = {
			'email': 'email',
			'password': 'password',
			'first_name': 'first_name',
		}
		serializer = RegisterCustomerRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_extra_field(self):
		data = {
			'email': 'email@email.com',
			'password': 'password',
			'first_name': 'first_name',
			'last_name': 'last_name',
			'extra_field': 'extra_field'
		}
		serializer = RegisterCustomerRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		validated_data = serializer.validated_data
		self.assertEqual(validated_data['email'], data['email'])
		self.assertEqual(validated_data['password'], data['password'])
		self.assertEqual(validated_data['first_name'], data['first_name'])
		self.assertEqual(validated_data['last_name'], data['last_name'])




