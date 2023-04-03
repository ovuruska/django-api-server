from datetime import date

from django.test import TestCase

from capacity.serializers.responses.base import CapacityBaseResponseSerializer


class CapacityBaseResponseSerializerTestCase(TestCase):

	def test_valid_data(self):
		serializer = CapacityBaseResponseSerializer(data={

			'date': date.today(),
			'morning_capacity': 0.6,
			'afternoon_capacity': 0.8
		})
		self.assertTrue(serializer.is_valid())
		expected_data = {
			'date': date.today(),
			'morning_capacity': 0.6,
			'afternoon_capacity': 0.8
		}

	def test_invalid_data(self):
		serializer = CapacityBaseResponseSerializer(data={

			'date': 'invalid',
			'morning_capacity': 0.6,
			'afternoon_capacity': 0.8
		})
		self.assertFalse(serializer.is_valid())


	def test_invalid_with_empty_object(self):
		serializer = CapacityBaseResponseSerializer(data={})
		self.assertFalse(serializer.is_valid())

	def test_invalid_with_missing_morning_capacity(self):
		serializer = CapacityBaseResponseSerializer(data={
			'date': date.today(),
			'afternoon_capacity': 0.8
		})
		self.assertFalse(serializer.is_valid())

	def test_invalid_with_missing_afternoon_capacity(self):
		serializer = CapacityBaseResponseSerializer(data={
			'date': date.today(),
			'morning_capacity': 0.6
		})
		self.assertFalse(serializer.is_valid())
