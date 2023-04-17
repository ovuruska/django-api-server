from datetime import datetime, timezone

from django.test import TestCase

from customer.serializers.requests.appointment import CustomerAppointmentRequestSerializer
from faker import Faker
# Get random time from future
faker = Faker()
faker.random.seed(0)
start = faker.future_datetime(end_date="+30d", tzinfo=timezone.utc)

class CustomerAppointmentResponseSerializerTestCase(TestCase):
	def test_valid(self):
		data = {
			"pet": 1,
			"products": [1, 2, 3],
			"start": str(start),
			"branch": 1,
			"service": "Grooming",
			"employee": 1
		}

		serializer = CustomerAppointmentRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		validated_data = serializer.validated_data
		self.assertEqual(validated_data["pet"], 1)
		self.assertEqual(validated_data["products"], [1, 2, 3])
		self.assertEqual(validated_data["start"],start)
		self.assertEqual(validated_data["employee"], 1)
		self.assertEqual(validated_data["branch"], 1)

	def test_invalid_no_pet(self):
		data = {
			"products": [1, 2, 3],
			"start":str(start),
			"branch": 1,
			"service": "Corte de pelo",
			"employee": 1
		}

		serializer = CustomerAppointmentRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_valid_no_products(self):

		data = {
			"pet": 1,
			"start": str(start),
			"branch": 1,
			"service": "Grooming",
			"employee": 1
		}

		serializer = CustomerAppointmentRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		validated_data = serializer.validated_data
		self.assertEqual(validated_data["pet"], 1)
		self.assertEqual(validated_data["products"], [])
		self.assertEqual(validated_data["start"],start)
		self.assertEqual(validated_data["employee"], 1)
		self.assertEqual(validated_data["branch"], 1)

	def test_invalid_no_start(self):
		data = {
			"pet": 1,
			"products": [1, 2, 3],
			"branch": 1,
			"service": "Grooming",
			"employee": 1
		}

		serializer = CustomerAppointmentRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_invalid_past_start(self):
		data = {
			"pet": 1,
			"products": [1, 2, 3],
			"start": "2019-01-01T00:00:00Z",
			"branch": 1,
			"service": "Grooming",
			"employee": 1
		}

		serializer = CustomerAppointmentRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())


	def test_valid_customer_notes(self):
		data = {
			"pet": 1,
			"products": [1, 2, 3],
			"start": str(start),
			"branch": 1,
			"service": "Grooming",
			"employee": 1,
			"customer_notes": "Notas del cliente"

		}
		serializer = CustomerAppointmentRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		validated_data = serializer.validated_data

		self.assertEqual(validated_data["customer_notes"], "Notas del cliente")

	def test_invalid(self):
		data= {'start': '2020-01-01T00:00:00Z', 'pet': 1, 'branch': 1, 'employee': 1, 'products': [1], 'customer_notes': 'Notes'}
		serializer = CustomerAppointmentRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_valid_start_without_tzinfo(self):
		start = faker.future_datetime(end_date="+30d")
		data = {
			"pet": 1,
			"products": [1, 2, 3],
			"start": str(start),
			"branch": 1,
			"service": "Grooming",
			"employee": 1
		}

		serializer = CustomerAppointmentRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())


	def test_invalid_grooming_without_employee(self):
		data = {
			"pet": 1,
			"products": [1, 2, 3],
			"start": str(start),
			"branch": 1,
			"service": "Grooming",
		}

		serializer = CustomerAppointmentRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

	def test_valid_wewash_without_employee(self):
		data = {
			"pet": 1,
			"products": [1, 2, 3],
			"start": str(start),
			"branch": 1,
			"service": "We Wash",
		}
		serializer = CustomerAppointmentRequestSerializer(data=data)
		self.assertTrue(serializer.is_valid())

	def test_invalid_service_name(self):
		data = {
			"pet": 1,
			"products": [1, 2, 3],
			"start": str(start),
			"branch": 1,
			"service": "Corte de pelo",
			"employee": 1
		}
		serializer = CustomerAppointmentRequestSerializer(data=data)
		self.assertFalse(serializer.is_valid())

