from datetime import datetime, timezone

# Path: customer/tests/serializers/responses/test_appts_response.py

from django.test import TestCase

from customer.serializers.responses.appt_response import CustomerAppointmentResponseSerializer


class CustomerAppointmentResponseSerializerTest(TestCase):



	def test_invalid_empty(self):
		data = {}
		serializer = CustomerAppointmentResponseSerializer(data=data)
		self.assertFalse(serializer.is_valid())
