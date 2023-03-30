from django.test import TestCase

from capacity.serializers.requests.monthly_capacity import MonthlyCapacityRequestSerializer

class MonthlyCapacityRequestSerializerTestCase(TestCase):

	def test_with_valid_data(self):
		data = {'employees': [1, 2], 'branches': [1, 2], 'service': 'service', 'date': '2023-04-01', }
		serializer = MonthlyCapacityRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		self.assertEqual(serializer.validated_data['employees'], [1, 2])
		self.assertEqual(serializer.validated_data['branches'], [1, 2])
		self.assertEqual(serializer.validated_data['service'], 'service')
		self.assertEqual(serializer.validated_data['date'], '2023-04-01')

	def test_with_empty_employees(self):
		data = { 'branches': [1, 2], 'service': 'service', 'date': '2023-04-01', }
		serializer = MonthlyCapacityRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())

	def test_with_empty_employees_and_branches(self):
		data = { 'service': 'service', 'date': '2023-04-01', }
		serializer = MonthlyCapacityRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())

	def test_with_empty_service_should_fail(self):
		data = { 'employees': [1, 2], 'branches': [1, 2], 'date': '2023-04-01', }
		serializer = MonthlyCapacityRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_with_empty_date_should_fail(self):

		data = { 'employees': [1, 2], 'branches': [1, 2], 'service': 'service', }
		serializer = MonthlyCapacityRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_with_empty_data_should_fail(self):
		data = {}
		serializer = MonthlyCapacityRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())