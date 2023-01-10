from django.test import TestCase

from scheduling.models import Customer, Appointment, Branch, Employee, Dog


class EmailConfirmationTestCase(TestCase):

	def setUp(self):
		customer = Customer.objects.create(
			name="John",
			email="oguzvuruskaner@gmail.com",
			uid="1234"
		)
		customer.save()
		branch = Branch.objects.create(
			name="Test Branch",
			address="Test Address",
			tubs=8,
		)
		branch.save()
		employee = Employee.objects.create(
			name="John Doe",
			email="",
			branch=branch,
			role="Full Grooming",
		)
		employee.save()
		dog = Dog.objects.create(
			name="Test Dog",
			breed="Test Breed",
			age=1,
			weight=1,
			owner=customer,


		)
		dog.save()



	def test_send_email(self):
		response = self.client.post('/api/appointment', data={
			"customer__id": 1,
			"branch": 1,
			"employee": 1,
			"dog": 1,
			"date": "2019-01-01",
			"service": "Full Grooming",

		})
		self.assertEqual(response.status_code, 201)

		self.ass
