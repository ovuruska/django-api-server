from datetime import date
from django.test import TestCase

from capacity.serializers.responses.monthly_capacity import MonthlyCapacityResponseSerializer


class MonthlyCapacityResponseSerializerTestCase(TestCase):
	def test_valid_data(self):
		data = {'date': date(2023, 4, 1), 'branch': 1, 'employee': 2, }
		serializer = MonthlyCapacityResponseSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		self.assertEqual(serializer.validated_data['date'], date(2023, 4, 1))
		self.assertEqual(serializer.validated_data['branch'], 1)
		self.assertEqual(serializer.validated_data['employee'], 2)

	def test_valid_data_with_number_string(self):
		data = {'date': '2023-04-01', 'branch': '1', 'employee': '2', }
		serializer = MonthlyCapacityResponseSerializer(data=data)
		self.assertTrue(serializer.is_valid())

	def test_invalid_string_data(self):
		data = {'date': '2023-04-01', 'branch': '1q', 'employee': '2', }
		serializer = MonthlyCapacityResponseSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_with_missing_data(self):
		data = {'date': '2023-04-01', 'branch': '1', }
		serializer = MonthlyCapacityResponseSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_with_list_data(self):
		data = {'date': ['2023-04-01'], 'branch': ['1'], 'employee': ['2'], }
		serializer = MonthlyCapacityResponseSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_with_empty_data(self):
		data = {}
		serializer = MonthlyCapacityResponseSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_with_list_data_multiple_items(self):
		data = {'date': ['2023-04-01', '2023-04-02'], 'branch': ['1', '2'], 'employee': ['2', '3'], }
		serializer = MonthlyCapacityResponseSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_with_list_data_multiple_items_with_one_invalid(self):
		data = {'date': ['2023-04-01', '2023-04-02'], 'branch': ['1', '2q'], 'employee': ['2', '3'], }
		serializer = MonthlyCapacityResponseSerializer(data=data)
		self.assertFalse(serializer.is_valid())
	
	def test_with_serializer_many(self):
		data = [
			{'date': '2023-04-01', 'branch': '1', 'employee': '2', },
			{'date': '2023-04-02', 'branch': '1', 'employee': '2', },
		]
		serializer = MonthlyCapacityResponseSerializer(data=data, many=True)
		self.assertTrue(serializer.is_valid())