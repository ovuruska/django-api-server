from datetime import datetime

from django.test import TestCase

from scheduling.models import Branch, Appointment, Employee, Dog, Customer


class ScheduleTestCase(TestCase):

	def setUp(self) -> None:
		Branch.objects.create(name="branch1", address="address1", description="description1", tubs=1)


	def test_empty_schedule(self):

		# Create a schedule with a single event
		response = self.client.get('/api/schedule/1')
		self.assertEqual(response.status_code, 422)

		response = self.client.get('/api/schedule/1?start=2020-01-01&end=2020-01-02')
		self.assertEqual(response.status_code, 200)

	def test_schedule(self):
		Branch.objects.create(name="branch2", address="address1", description="description1", tubs=1)
		Employee.objects.create(name="employee1", email="qw@qwe.cq", phone="1231231231", branch=Branch.objects.get(name="branch1"))
		Customer.objects.create(name="customer1", email="qweq@ç.com", phone="1231231231")
		Dog.objects.create(name="dog1", breed="breed1", age=1, weight=1,owner=Customer.objects.get(name="customer1"))
		Appointment.objects.create(
			branch=Branch.objects.get(name="branch1"),
			start=datetime(2020, 1, 1, 10, 0, 0),
			end=datetime(2020, 1, 1, 11, 0, 0),
			employee=Employee.objects.get(name="employee1"),
			dog=Dog.objects.get(name="dog1"),
			customer=Customer.objects.get(name="customer1"),
		)
		response = self.client.get('/api/schedule/1?start=2020-01-01&end=2020-01-02')
		self.assertEqual(response.status_code, 200)
		response_data = response.json()
		self.assertEqual(len(response_data), 1)

		free_hours = response_data[0]
		self.assertEqual(sum(free_hours),1)
		self.assertEqual(free_hours[1], 1)
