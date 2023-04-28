from datetime import datetime

from django.test import TestCase

from customer.serializers.requests.pet import CreatePetRequestSerializer


class CreatePetRequestSerializerTestCase(TestCase):

	def test_valid_data(self):
		data = {
			"name": "Fido",
			"breed": "Poodle",
			"weight": 10,
			"birth_date": "2019-01-01",
			"gender":"Male"
		}

		serializer = CreatePetRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		validated_data = serializer.validated_data
		self.assertEqual(validated_data["name"], data["name"])
		self.assertEqual(validated_data["breed"], data["breed"])
		self.assertEqual(validated_data["weight"], data["weight"])
		self.assertEqual(validated_data["birth_date"], datetime.strptime(data["birth_date"],"%Y-%m-%d").date())
		self.assertEqual(validated_data["gender"],data["gender"])

	def test_valid_data_with_special_handling(self):
		data = {
			"name": "Fido",
			"breed": "Poodle",
			"weight": 10,
			"birth_date": "2019-01-01",
			"gender": "Male",
			"special_handling": "test"
		}
		serializer = CreatePetRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		validated_data = serializer.validated_data
		self.assertEqual(validated_data["name"], data["name"])
		self.assertEqual(validated_data["breed"], data["breed"])
		self.assertEqual(validated_data["weight"], data["weight"])
		self.assertEqual(validated_data["birth_date"], datetime.strptime(data["birth_date"],"%Y-%m-%d").date())
		self.assertEqual(validated_data["gender"],data["gender"])
		self.assertEqual(validated_data["special_handling"],data["special_handling"])

	def test_valid_data_with_special_handling_with_1000_chars(self):
		data = {
			"name": "Fido",
			"breed": "Poodle",
			"weight": 10,
			"birth_date": "2019-01-01",
			"gender": "Male",
			"special_handling": 1000*"q"
		}
		serializer = CreatePetRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		validated_data = serializer.validated_data
		self.assertEqual(validated_data["name"], data["name"])
		self.assertEqual(validated_data["breed"], data["breed"])
		self.assertEqual(validated_data["weight"], data["weight"])
		self.assertEqual(validated_data["birth_date"], datetime.strptime(data["birth_date"], "%Y-%m-%d").date())
		self.assertEqual(validated_data["gender"], data["gender"])
		self.assertEqual(validated_data["special_handling"], data["special_handling"])

	def test_invalid_data_with_special_handling_with_1001_chars(self):
		data = {
			"name": "Fido",
			"breed": "Poodle",
			"weight": 10,
			"birth_date": "2019-01-01",
			"gender": "Male",
			"special_handling": 1001 * "q"
		}
		serializer = CreatePetRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

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


	def test_with_rabies_vacination_field(self):
		data = {
			"name": "Fido",
			"breed": "Poodle",
			"weight": 10,
			"age": 2,
			"gender": "invalid",
			"rabies_vaccination": "2019-01-01"
		}
		serializer = CreatePetRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		validated_data = serializer.validated_data
		self.assertEqual(validated_data["rabies_vaccination"], datetime.strptime(data["rabies_vaccination"],"%Y-%m-%d").date())
