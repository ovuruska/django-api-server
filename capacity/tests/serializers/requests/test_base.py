from django.test import TestCase

from capacity.serializers.requests.base import BaseRequestSerializer


class BaseRequestSerializerTestCase(TestCase):
	def test_check_valid(self   ):
		# Create a serializer with valid data
		serializer = BaseRequestSerializer(data={
			"employees": [1, 2, 3],
			"branches": [1, 2, 3],
			"service": "Full Grooming",
			"date": "01/2020",
		})
		# Check that the serializer is valid
		self.assertTrue(serializer.is_valid())

	def test_check_invalid_without_date(self):
		# Create a serializer with invalid data
		serializer = BaseRequestSerializer(data={
			"employees": [1, 2, 3],
			"branches": [1, 2, 3],
			"service": "Full Grooming",
		})
		# Check that the serializer is invalid
		self.assertFalse(serializer.is_valid())

	def test_check_invalid_without_service(self):
		# Create a serializer with invalid data
		serializer = BaseRequestSerializer(data={
			"employees": [1, 2, 3],
			"branches": [1, 2, 3],
			"date": "01/2020",
		})
		# Check that the serializer is invalid
		self.assertFalse(serializer.is_valid())

	def test_valid_without_branches(self):
		self.assertTrue(BaseRequestSerializer(data={
			"employees": [1, 2, 3],
			"service": "Full Grooming",
			"date": "01/2020",
		}).is_valid())

	def test_valid_without_employees(self):
		self.assertTrue(BaseRequestSerializer(data={
			"branches": [1, 2, 3],
			"service": "Full Grooming",
			"date": "01/2020",
		}).is_valid())

	def test_valid_without_employees_or_branches(self):
		self.assertTrue(BaseRequestSerializer(data={
			"service": "Full Grooming",
			"date": "01/2020",
		}).is_valid())


	def test_invalid_with_extra_field(self):
		self.assertFalse(BaseRequestSerializer(data={
			"employees": [1, 2, 3],
			"branches": [1, 2, 3],
			"service": "Full Grooming",
			"date": "01/2020",
			"extra": "extra",
		}).is_valid())
