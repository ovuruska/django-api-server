from django.test import TestCase

from customer.serializers.responses.pet_details import CustomerPetDetailsResponseSerializer



class CustomerPetDetailsResponseSerializerTestCase(TestCase):
	data = {
		"id": 1,
		"created_at": "2019-01-01T00:00:00Z",
		"updated_at": "2019-01-01T00:00:00Z",
		"name": "name",
		"breed": "breed",
		"age": 1,
		"weight": 1,
		"description": "description",
		"rabies_vaccination": "2019-01-01T00:00:00Z",
		"employee_notes": "employee_notes",
		"customer_notes": "customer_notes",
		"special_handling": True,
		"coat_type": "coat_type",
		"owner": 1,
		"number_of_groomings": 1,
		"number_of_wewashes": 1,
		"total_grooming_cost": 1,
		"total_wewash_cost": 1,
	}
	def test_valid(self):

		serializer = CustomerPetDetailsResponseSerializer(data=self.data)
		self.assertTrue(serializer.is_valid())
		validated_data = serializer.validated_data
		self.assertEqual(validated_data["id"],self.data["id"])
		self.assertEqual(validated_data["name"],self.data["name"])
		self.assertEqual(validated_data["breed"],self.data["breed"])
		self.assertEqual(validated_data["age"],self.data["age"])
		self.assertEqual(validated_data["weight"],self.data["weight"])
		self.assertEqual(validated_data["description"],self.data["description"])
		self.assertEqual(validated_data["employee_notes"],self.data["employee_notes"])
		self.assertEqual(validated_data["customer_notes"],self.data["customer_notes"])
		self.assertEqual(validated_data["special_handling"],self.data["special_handling"])
		self.assertEqual(validated_data["coat_type"],self.data["coat_type"])
		self.assertEqual(validated_data["owner"],self.data["owner"])
		self.assertEqual(validated_data["number_of_groomings"],self.data["number_of_groomings"])
		self.assertEqual(validated_data["number_of_wewashes"],self.data["number_of_wewashes"])
		self.assertEqual(validated_data["total_grooming_cost"],self.data["total_grooming_cost"])
		self.assertEqual(validated_data["total_wewash_cost"],self.data["total_wewash_cost"])


	def test_valid_multiple(self):

		serializer = CustomerPetDetailsResponseSerializer(data=[self.data,self.data],many=True)
		self.assertTrue(serializer.is_valid())
		validated_list = serializer.validated_data
		for validated_data in validated_list:
			self.assertEqual(validated_data["id"], self.data["id"])
			self.assertEqual(validated_data["name"], self.data["name"])
			self.assertEqual(validated_data["breed"], self.data["breed"])
			self.assertEqual(validated_data["age"], self.data["age"])
			self.assertEqual(validated_data["weight"], self.data["weight"])
			self.assertEqual(validated_data["description"], self.data["description"])
			self.assertEqual(validated_data["employee_notes"], self.data["employee_notes"])
			self.assertEqual(validated_data["customer_notes"], self.data["customer_notes"])
			self.assertEqual(validated_data["special_handling"], self.data["special_handling"])
			self.assertEqual(validated_data["coat_type"], self.data["coat_type"])
			self.assertEqual(validated_data["owner"], self.data["owner"])
			self.assertEqual(validated_data["number_of_groomings"], self.data["number_of_groomings"])
			self.assertEqual(validated_data["number_of_wewashes"], self.data["number_of_wewashes"])
			self.assertEqual(validated_data["total_grooming_cost"], self.data["total_grooming_cost"])
			self.assertEqual(validated_data["total_wewash_cost"], self.data["total_wewash_cost"])
