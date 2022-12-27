import urllib.parse
from django.test import TestCase

from scheduling.common import Mock
from scheduling.models import Appointment


class AppointmentFilterTestCase(TestCase):

	root_url = "/api/schedule/appointments"

	def setUp(self) :
		self.mock = Mock()
		self.data = self.mock.generate()

	def test_get_all(self):
		response = self.client.get(self.root_url+"?")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), self.mock.number_of_appointments)

	def test_get_all_by_employee(self):
		employees = self.data["employees"]
		employee_name = employees[0].name
		response = self.client.get(self.root_url+"?employee__name="+employee_name)
		self.assertEqual(response.status_code, 200)
		data = response.data
		for appointment in data:
			self.assertEqual(appointment["employee"]["name"], employee_name)

	def test_get_all_by_branch_name(self):
		branches = self.data["branches"]
		branch_name = branches[0].name
		response = self.client.get(self.root_url+"?branch__name="+branch_name)
		self.assertEqual(response.status_code, 200)
		data = response.data
		for appointment in data:
			self.assertEqual(appointment["branch"]["name"], branch_name)




	def test_get_all_by_dog_breed(self):
		dogs = self.data["dogs"]
		dog_breed = dogs[0].breed
		response = self.client.get(self.root_url+"?dog__breed="+dog_breed)
		self.assertEqual(response.status_code, 200)
		data = response.data
		for appointment in data:
			self.assertEqual(appointment["dog"]["breed"], dog_breed)



	def test_get_all_by_creation_time(self):

		response = self.client.get(self.root_url+"?created_at__gte=2019-01-01")
		self.assertEqual(response.status_code, 200)
		data = response.data
		for appointment in data:
			self.assertGreaterEqual(appointment["created_at"], "2019-01-01")



	def test_get_all_by_status(self):
		response = self.client.get(self.root_url+"?status=Pending")
		self.assertEqual(response.status_code, 200)
		data = response.data


		for appointment in data:
			self.assertEqual(appointment["status"], "Pending")


	def test_get_all_by_appointment_date(self):
		response = self.client.get(self.root_url+"?start__gte=2019-01-01")
		self.assertEqual(response.status_code, 200)
		data = response.data

		for appointment in data:
			self.assertGreaterEqual(appointment["start"], "2019-01-01")


		response = self.client.get(self.root_url+"?start__lte=2019-01-01")
		self.assertEqual(response.status_code, 200)
		data = response.data
		for appointment in data:
			self.assertLessEqual(appointment["start"], "2019-01-01")

	def test_get_all_by_appointment_type(self):
		service_type = "WeWash"
		query =self.root_url+f"?appointment_type={service_type}"
		query = urllib.parse.quote(query)
		response = self.client.get(query)
		print(query)
		self.assertEqual(response.status_code, 200)
		data = response.data
		for appointment in data:
			self.assertEqual(appointment["appointment_type"], service_type)

		service_type = "Full Grooming"

		response = self.client.get(self.root_url+f"?appointment_type={service_type}")
		self.assertEqual(response.status_code, 200)
		data = response.data
		for appointment in data:
			self.assertEqual(appointment["appointment_type"], service_type)

		service_type = "Invalid"

		response = self.client.get(self.root_url+f"?appointment_type={service_type}")
		self.assertEqual(response.status_code, 200)
		data = response.data
		for appointment in data:
			self.assertEqual(appointment["appointment_type"], service_type)
