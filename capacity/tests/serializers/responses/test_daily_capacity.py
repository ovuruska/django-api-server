from datetime import date

from django.apps import apps
from django.test import TestCase
from capacity.serializers.responses.daily_capacity import DailyCapacityResponseSerializer

Branch = apps.get_model('scheduling', 'Branch')
class DailyCapacityResponseSerializerTestCase(TestCase):

	def test_with_valid_data(self):
		serializer = DailyCapacityResponseSerializer(data={
			'date': date.today(),
			'morning_capacity': 0.6,
			'afternoon_capacity': 0.8,
			'branch': {
				'id': 1,
				'name': 'branch1',
			}
		})
		self.assertTrue(serializer.is_valid())

	def test_with_missing_branch(self):
		serializer = DailyCapacityResponseSerializer(data={
			'date': date.today(),
			'morning_capacity': 0.6,
			'afternoon_capacity': 0.8
		})
		self.assertFalse(serializer.is_valid())

