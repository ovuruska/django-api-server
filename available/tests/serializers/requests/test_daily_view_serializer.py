import datetime
from django.test import TestCase

from available.serializers.requests.daily_view import DailyViewRequestSerializer


class DailyViewSerializerTestCase(TestCase):

	def get_future_date(self) -> str:
		future_date = datetime.date.today() + datetime.timedelta(days=1)
		return future_date.strftime('%Y-%m-%d')

	def test_valid_data(self):
		data = {
			'employees': [1, 2, 3],
			'branches': [1, 2, 3],
			'service': 'We Wash',
			'date': self.get_future_date()
		}

		serializer = DailyViewRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())


	def test_invalid_service(self):
		data = {
			'employees': [1, 2, 3],
			'branches': [1, 2, 3],
			'service': 'Invalid Service',
			'date': self.get_future_date()
		}

		serializer = DailyViewRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())


	def test_past_date(self):
		data = {
			'employees': [1, 2, 3],
			'branches': [1, 2, 3],
			'service': 'We Wash',
			'date': '2020-01-01'
		}

		serializer = DailyViewRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())

	def test_empty_employees(self):

		data = {
			'employees': [],
			'branches': [1, 2, 3],
			'service': 'We Wash',
			'date': self.get_future_date()
		}

		serializer = DailyViewRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())

	def test_empty_branches(self):
		data = {
			'employees': [1, 2, 3],
			'branches': [],
			'service': 'We Wash',
			'date': self.get_future_date()
		}

		serializer = DailyViewRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())

	def test_empty_branches_and_employees(self):
		data = {
			'employees': [],
			'branches': [],
			'service': 'We Wash',
			'date': self.get_future_date()
		}

		serializer = DailyViewRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())


	def test_invalid_no_service(self):
		data = {
			'employees': [1, 2, 3],
			'branches': [1, 2, 3],
			'date': self.get_future_date()
		}

		serializer = DailyViewRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())


	def test_invalid_no_date(self):
		data = {
			'employees': [1, 2, 3],
			'branches': [1, 2, 3],
			'service': 'We Wash',
		}

		serializer = DailyViewRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_empty_object(self):
		data = {}

		serializer = DailyViewRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())


	def test_with_duration(self):
		data = {
			'employees': [1, 2, 3],
			'branches': [1, 2, 3],
			'service': 'We Wash',
			'date': self.get_future_date(),
			'duration': 120
		}

		serializer = DailyViewRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())

	def test_with_negative_duration_fails(self):
		data = {
			'employees': [1, 2, 3],
			'branches': [1, 2, 3],
			'service': 'We Wash',
			'date': self.get_future_date(),
			'duration': -120
		}

		serializer = DailyViewRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

