from django.test import TestCase

from available.serializers.responses.daily_view import DailyViewResponseSerializer


class DailyViewResponseSerializerTestCase(TestCase):

	def test_valid_data(self):

		data = {
			'start': '2019-01-01 00:00:00',
			'end': '2019-01-01 00:00:00',
			'employee': 1,
			'branch': 1
		}
		serializer = DailyViewResponseSerializer(data=data)
		self.assertTrue(serializer.is_valid())

	def test_invalid_start(self):
		data = {
			'start': 'Invalid Date',
			'end': '2019-01-01 00:00:00',
			'employee': 1,
			'branch': 1
		}
		serializer = DailyViewResponseSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_invalid_end(self):
		data = {
			'start': '2019-01-01 00:00:00',
			'end': 'Invalid Date',
			'employee': 1,
			'branch': 1
		}
		serializer = DailyViewResponseSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_empty_object(self):
		data = {}
		serializer = DailyViewResponseSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_empty_employee(self):
		data = {
			'start': '2019-01-01 00:00:00',
			'end': '2019-01-01 00:00:00',
			'branch': 1

		}
		serializer = DailyViewResponseSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_empty_branch(self):
		data = {
			'start': '2019-01-01 00:00:00',
			'end': '2019-01-01 00:00:00',
			'employee': 1
		}
		serializer = DailyViewResponseSerializer(data=data)
		self.assertFalse(serializer.is_valid())
