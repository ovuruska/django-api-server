from django.test import TestCase
from capacity.serializers.requests.monthly_capacity import MonthlyCapacityRequestSerializer

class MonthlyCapacityRequestSerializerTestCase(TestCase):

	def test_with_invalid_service_name(self):
		data = {'employees': [1, 2], 'branches': [1, 2], 'service': 'service', 'date': '2023-04-01', }
		serializer = MonthlyCapacityRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_invalid_date_format(self):
		data = {'employees': [1, 2], 'branches': [1, 2], 'service': 'Full Grooming', 'date': '2023/04/01', }
		serializer = MonthlyCapacityRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())


	def test_with_empty_service_should_fail(self):
		data = { 'employees': [1, 2], 'branches': [1, 2], 'date': '2023-04-01', }
		serializer = MonthlyCapacityRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_with_empty_date_should_fail(self):

		data = { 'employees': [1, 2], 'branches': [1, 2], 'service': 'service', }
		serializer = MonthlyCapacityRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_with_empty_data_should_fail(self):
		data = {}
		serializer = MonthlyCapacityRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())


	def test_with_invalid_date_format(self):
		data = {'employees': [1, 2], 'branches': [1, 2], 'service': 'service', 'date': '2023/04/01', }
		serializer = MonthlyCapacityRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())


	def test_with_invalid_service_should_fail(self):
		data = {'employees': [1, 2], 'branches': [1, 2], 'service': 'invalid', 'date': '2023-04-01', }
		serializer = MonthlyCapacityRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_with_valid_data_2(self):
		data = {'employees': [1, 2], 'branches': [1, 2], 'service': 'We Wash', 'date': '04/2023', }
		serializer = MonthlyCapacityRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		self.assertEqual(serializer.validated_data['employees'], [1, 2])
		self.assertEqual(serializer.validated_data['branches'], [1, 2])
		self.assertEqual(serializer.validated_data['service'], 'We Wash')
		self.assertEqual(serializer.validated_data['date'], '04/2023')


	def test_with_valid_data(self):
		data = {'employees': [1, 2], 'branches': [1, 2], 'service': 'Full Grooming', 'date': '04/2023', }
		serializer = MonthlyCapacityRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		self.assertEqual(serializer.validated_data['employees'], [1, 2])
		self.assertEqual(serializer.validated_data['branches'], [1, 2])
		self.assertEqual(serializer.validated_data['service'], 'Full Grooming')
		self.assertEqual(serializer.validated_data['date'], '04/2023')


	def test_with_empty_employees_valid(self):
		data = {'branches': [1, 2], 'service': 'Full Grooming', 'date': '04/2023', }
		serializer = MonthlyCapacityRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		self.assertEqual(serializer.validated_data['employees'], [])
		self.assertEqual(serializer.validated_data['branches'], [1, 2])
		self.assertEqual(serializer.validated_data['service'], 'Full Grooming')
		self.assertEqual(serializer.validated_data['date'], '04/2023')

	def test_with_empty_employees_and_branches_valid(self):
		data = {'service': 'Full Grooming', 'date': '04/2023', }
		serializer = MonthlyCapacityRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		self.assertEqual(serializer.validated_data['employees'], [])
		self.assertEqual(serializer.validated_data['branches'], [])
		self.assertEqual(serializer.validated_data['service'], 'Full Grooming')
		self.assertEqual(serializer.validated_data['date'], '04/2023')


	def test_invalid_with_extra_fields(self):
		data = {'employees': [1, 2], 'branches': [1, 2], 'service': 'Full Grooming', 'date': '04/2023', 'extra': 'extra'}
		serializer = MonthlyCapacityRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())