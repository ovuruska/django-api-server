from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from scheduling.models import Appointment, Customer, Dog, Product, Service, Branch, Employee
from scheduling.tests.views.appointment.base import BaseTestCase


class AppointmentEmployeeCreateAPIViewTestCase(BaseTestCase):

	def test_create_appointment(self):
		data = {
			"customer_name": "John Doe",
			"customer_email": "john.doe@example.com",
			"customer_phone": "123-456-7890",
			"dog_name": "Fido",
			"dog_breed": "Golden Retriever",
			"start": "2023-04-01T12:00:00Z",
			"end": "2023-04-01T13:00:00Z",
			"employee_id": 1,  # Replace with a valid employee ID
			"branch_id": 1,  # Replace with a valid branch ID
			"products": [self.product.id],
			"services": [self.service.id],
			"tip": "5.00",
		}
		response = self.client.post(self.url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(Appointment.objects.count(), 1)
		appointment = Appointment.objects.first()
		self.assertEqual(appointment.cost, Decimal('35.00'))

	def test_create_appointment_with_missing_data(self):
		data = {
			"customer_name": "John Doe",
			"dog_name": "Fido",
		}
		response = self.client.post(self.url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


