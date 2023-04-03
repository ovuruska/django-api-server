from capacity.serializers.requests.daily_capacity import DailyCapacityRequestSerializer
from django.test import TestCase

class DailyCapacityRequestSerializerTestCase(TestCase):

	def test_serializer_base_case(self):
		data = {
			'date': '2019-01-01',
			'service': 'Full Grooming',
		}
		serializer = DailyCapacityRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())

		expected_data = {
			'branches': [],
			'employees': [],
			'date': '2019-01-01',
			'service': 'Full Grooming',
		}
		self.assertEqual(serializer.validated_data, expected_data)


	def test_serializer_with_employees(self):
		data = {
			'date': '2019-01-01',
			'service': 'Full Grooming',
			'employees': [1, 2, 3],
		}
		serializer = DailyCapacityRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())

		expected_data = {
			'branches': [],
			'employees': [1, 2, 3],
			'date': '2019-01-01',
			'service': 'Full Grooming',
		}
		self.assertEqual(serializer.validated_data, expected_data)

		expected_data = {
			'branches': [],
			'employees': [1, 2, 3],
			'date': '2019-01-01',
			'service': 'Full Grooming',

		}
		self.assertEqual(serializer.validated_data, expected_data)

	def test_serializer_with_employees_and_branches(self):
		data = {
			'date': '2019-01-01',
			'service': 'Full Grooming',
			'employees': [1, 2, 3],
			'branches': [1, 2, 3],
		}
		serializer = DailyCapacityRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())

		expected_data = {
			'branches': [1, 2, 3],
			'employees': [1, 2, 3],
			'date': '2019-01-01',
			'service': 'Full Grooming',
		}
		self.assertEqual(serializer.validated_data, expected_data)

	def test_serializer_with_branches(self):
		data = {
			'date': '2019-01-01',
			'service': 'Full Grooming',
			'branches': [1, 2, 3],
		}
		serializer = DailyCapacityRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())

		expected_data = {
			'branches': [1, 2, 3],
			'employees': [],
			'date': '2019-01-01',
			'service': 'Full Grooming',
		}
		self.assertEqual(serializer.validated_data, expected_data)

	def test_serializer_with_invalid_date(self):
		data = {
			'date': '2019-01',
			'service': 'Full Grooming',
		}
		serializer = DailyCapacityRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_serializer_with_inbvalid_date_2(self):
		data = {
			'date': '2019-01-01-01',
			'service': 'Full Grooming',
		}
		serializer = DailyCapacityRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())
	