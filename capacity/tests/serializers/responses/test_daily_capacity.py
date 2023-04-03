from datetime import date
from django.test import TestCase
from capacity.serializers.responses.daily_capacity import DailyCapacityResponseSerializer


class DailyCapacityResponseSerializerTestCase(TestCase):

	def test_with_valid_data(self):
		serializer = DailyCapacityResponseSerializer(data={
			'date': date.today(),
			'morning_capacity': 0.6,
			'afternoon_capacity': 0.8,
			'branch': 1
		})
		self.assertTrue(serializer.is_valid())
		expected_data = {
			'date': date.today(),
			'morning_capacity': 0.6,
			'afternoon_capacity': 0.8,
			'branch': 1
		}
		self.assertEqual(serializer.data, expected_data)

	def test_with_missing_branch(self):
		serializer = DailyCapacityResponseSerializer(data={
			'date': date.today(),
			'morning_capacity': 0.6,
			'afternoon_capacity': 0.8
		})
		self.assertFalse(serializer.is_valid())

