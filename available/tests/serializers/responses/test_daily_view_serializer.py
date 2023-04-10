import datetime
import zoneinfo

from django.test import TestCase

from available.serializers.responses.daily_view import DailyViewResponseSerializer

"""
class BranchNameSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField()
	class Meta:
		model = apps.get_model('scheduling', 'Branch')
		fields = ('id','name')

class EmployeeNameSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField()
	class Meta:
		model = apps.get_model('scheduling', 'Employee')
		fields = ('id','name')

"""
class DailyViewResponseSerializerTestCase(TestCase):

	def test_valid(self):
		data = {
			'start': '2019-01-01 00:00:00',
			'end':'2019-01-01 00:00:00',
			'employee': {
				'id': 1,
				'name': 'Test Employee'
			},
			'branch': {
				'id': 1,
				'name': 'Test Branch'
			}

		}
		serializer = DailyViewResponseSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		validated_data = serializer.validated_data
		self.assertEqual(validated_data['start'], datetime.datetime(2019, 1, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')))
		self.assertEqual(validated_data['end'],  datetime.datetime(2019, 1, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')))
		self.assertEqual(validated_data['employee'], data['employee'])
		self.assertEqual(validated_data['branch'], data['branch'])



	def test_invalid_data_with_ids(self):

		data = {
			'start': '2019-01-01 00:00:00',
			'end': '2019-01-01 00:00:00',
			'employee': 1,
			'branch': 1
		}
		serializer = DailyViewResponseSerializer(data=data)
		self.assertFalse(serializer.is_valid())

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
