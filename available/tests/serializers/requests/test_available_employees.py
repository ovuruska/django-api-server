"""
from rest_framework import serializers


class AvailableEmployeesRequestSerializer(serializers.Serializer):
	date = serializers.DateTimeField()
	branches = serializers.ListField(child=serializers.IntegerField(), required=False)
	service = serializers.CharField()
	times = serializers.ListField(child=serializers.CharField(), required=False)


"""
"""
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

		serializers = DailyViewRequestSerializer(data=data)
		self.assertTrue(serializers.is_valid())


	def test_invalid_service(self):
		data = {
			'employees': [1, 2, 3],
			'branches': [1, 2, 3],
			'service': 'Invalid Service',
			'date': self.get_future_date()
		}

		serializers = DailyViewRequestSerializer(data=data)
		self.assertFalse(serializers.is_valid())


	def test_past_date(self):
		data = {
			'employees': [1, 2, 3],
			'branches': [1, 2, 3],
			'service': 'We Wash',
			'date': '2020-01-01'
		}

		serializers = DailyViewRequestSerializer(data=data)
		self.assertTrue(serializers.is_valid())

	def test_empty_employees(self):

		data = {
			'employees': [],
			'branches': [1, 2, 3],
			'service': 'We Wash',
			'date': self.get_future_date()
		}

		serializers = DailyViewRequestSerializer(data=data)
		self.assertTrue(serializers.is_valid())

	def test_empty_branches(self):
		data = {
			'employees': [1, 2, 3],
			'branches': [],
			'service': 'We Wash',
			'date': self.get_future_date()
		}

		serializers = DailyViewRequestSerializer(data=data)
		self.assertTrue(serializers.is_valid())

	def test_empty_branches_and_employees(self):
		data = {
			'employees': [],
			'branches': [],
			'service': 'We Wash',
			'date': self.get_future_date()
		}

		serializers = DailyViewRequestSerializer(data=data)
		self.assertTrue(serializers.is_valid())


	def test_invalid_no_service(self):
		data = {
			'employees': [1, 2, 3],
			'branches': [1, 2, 3],
			'date': self.get_future_date()
		}

		serializers = DailyViewRequestSerializer(data=data)
		self.assertFalse(serializers.is_valid())


	def test_invalid_no_date(self):
		data = {
			'employees': [1, 2, 3],
			'branches': [1, 2, 3],
			'service': 'We Wash',
		}

		serializers = DailyViewRequestSerializer(data=data)
		self.assertFalse(serializers.is_valid())

	def test_empty_object(self):
		data = {}

		serializers = DailyViewRequestSerializer(data=data)
		self.assertFalse(serializers.is_valid())


	def test_with_duration(self):
		data = {
			'employees': [1, 2, 3],
			'branches': [1, 2, 3],
			'service': 'We Wash',
			'date': self.get_future_date(),
			'duration': 120
		}

		serializers = DailyViewRequestSerializer(data=data)
		self.assertTrue(serializers.is_valid())

	def test_with_negative_duration_fails(self):
		data = {
			'employees': [1, 2, 3],
			'branches': [1, 2, 3],
			'service': 'We Wash',
			'date': self.get_future_date(),
			'duration': -120
		}

		serializers = DailyViewRequestSerializer(data=data)
		self.assertFalse(serializers.is_valid())
"""
# Path: available/tests/serializers/requests/test_daily_employees.py
from django.test import TestCase
class TestAvailableEmployees(TestCase):

	def test_valid_data(self):
		data = {
			'branches': [1, 2, 3],
			'service': 'We Wash',
			'date': '2020-01-01',
			'times': ['10:00', '11:00']
		}
