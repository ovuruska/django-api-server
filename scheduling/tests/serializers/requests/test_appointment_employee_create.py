from django.test import TestCase

from scheduling.serializers.Appointment import AppointmentEmployeeCreateSerializer


class AppoinmentEmployeeCreateSerializerTestCase(TestCase):
	valid_data = {
		"employee": 1,
		"branch": 1,
		"start": "2020-01-01T10:00:00Z",
		"end": "2020-01-01T11:00:00Z",
		"products": [1, 2],
		"service": "We wash",
		"pet": 1,
		"customer": 1
	}

	def test_valid(self):
		serializer = AppointmentEmployeeCreateSerializer(data=self.valid_data)
		is_valid = serializer.is_valid()
		self.assertTrue(is_valid  )


	def test_invalidate_start_date_after_end(self):
		data = dict(self.valid_data)
		data["start"] = "2020-01-01T11:00:00Z"
		data["end"] = "2020-01-01T10:00:00Z"

		serializer = AppointmentEmployeeCreateSerializer(data=data)
		is_valid = serializer.is_valid()
		self.assertFalse(is_valid)
