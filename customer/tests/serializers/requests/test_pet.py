
from django.test import TestCase

from customer.serializers.requests.pet import CreatePetRequestSerializer


class CreatePetRequestSerializerTestCase(TestCase):

	def test_valid_data(self):
		data = {
			"name": "Fido",
			"breed": "Poodle",
			"weight": 10,
			"age": 2,
			"gender":"Male"
		}

		serializer = CreatePetRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		validated_data = serializer.validated_data
		self.assertEqual(validated_data["name"], data["name"])
		self.assertEqual(validated_data["breed"], data["breed"])
		self.assertEqual(validated_data["weight"], data["weight"])
		self.assertEqual(validated_data["age"], data["age"])
		self.assertEqual(validated_data["gender"],data["gender"])

	def test_invalid_data_missing_fields(self):
		data = {
			"name": "Fido",
		}

		serializer = CreatePetRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_invalid_data_invalid_gender(self):
		data = {
			"name": "Fido",
			"breed": "Poodle",
			"weight": 10,
			"age": 2,
			"gender":"invalid"
		}
		serializer = CreatePetRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

