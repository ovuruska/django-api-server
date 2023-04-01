from datetime import date
from django.test import TestCase

from capacity.serializers.responses.monthly_capacity import MonthlyCapacityResponseSerializer


class MonthlyCapacityResponseSerializerTestCase(TestCase):

	def test_with_empty_object(self):
		serializer = MonthlyCapacityResponseSerializer(data={})
		self.assertFalse(serializer.is_valid())

	def test_with_valid_data(self):
		serializer = MonthlyCapacityResponseSerializer(data={
			'date': date.today(),
			'morning_capacity': 0.6,
			'afternoon_capacity': 0.8
		})
		self.assertTrue(serializer.is_valid())

	def test_with_invalid_date(self):
		serializer = MonthlyCapacityResponseSerializer(data={
			'date': 'invalid',
			'morning_capacity': 0.6,
			'afternoon_capacity': 0.8
		})
		self.assertFalse(serializer.is_valid())

	def test_with_invalid_morning_capacity(self):
		serializer = MonthlyCapacityResponseSerializer(data={
			'date': date.today(),
			'morning_capacity': '0.6',
			'afternoon_capacity': 0.8
		})
		self.assertTrue(serializer.is_valid())

	def test_with_list_morning_capacity(self):
		serializer = MonthlyCapacityResponseSerializer(data={
			'date': date.today(),
			'morning_capacity': [0.6],
			'afternoon_capacity': 0.8
		})
		self.assertFalse(serializer.is_valid())


	def test_with_invalid_afternoon_capacity(self):
		serializer = MonthlyCapacityResponseSerializer(data={
			'date': date.today(),
			'morning_capacity': 0.6,
			'afternoon_capacity': '0.8'
		})
		self.assertTrue(serializer.is_valid())

