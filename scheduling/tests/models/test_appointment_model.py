from django.utils import timezone
from django.test import TestCase
from faker import Faker

from scheduling.models import Appointment, Customer, Dog, Branch, Employee, Service, Product

"""
This tests suite contains three tests cases:

test_appointment_creation: Tests whether the Appointment instance is created correctly with the given data.
test_appointment_is_modifiable: Tests the is_modifiable method of the Appointment model.
test_appointment_is_available: Tests the is_available method of the Appointment model.
"""

class AppointmentModelTestCase(TestCase):
	def setUp(self):
		fake = Faker()

		self.customer = Customer.objects.create(name='John Doe', email='john.doe@example.com')
		self.dog = Dog.objects.create(name='Fido', breed='Golden Retriever', owner=self.customer)
		self.branch = Branch.objects.create(name='Main Branch', address='123 Main St')
		self.employee = Employee.objects.create(user=None)  # Assuming Employee has a nullable user field
		# duration = models.DurationField()


		self.service = Service.objects.create(name='Bath', description='Dog bath service', cost=25.0,  duration=fake.time_delta())

		self.product = Product.objects.create(name='Shampoo', description='Dog shampoo', cost=10.0)
		self.appointment = Appointment.objects.create(customer=self.customer, dog=self.dog, start=timezone.now(),
			end=timezone.now(), branch=self.branch, employee=self.employee, )
		self.appointment.services.add(self.service)
		self.appointment.products.add(self.product)


	def test_appointment_creation(self):
		self.assertIsNotNone(self.appointment)
		self.assertEqual(self.appointment.customer, self.customer)
		self.assertEqual(self.appointment.dog, self.dog)
		self.assertEqual(self.appointment.branch, self.branch)
		self.assertEqual(self.appointment.employee, self.employee)
		self.assertIn(self.service, self.appointment.services.all())
		self.assertIn(self.product, self.appointment.products.all())


	def test_appointment_is_modifiable(self):
		self.appointment.status = Appointment.Status.COMPLETED
		self.appointment.save()
		self.assertFalse(self.appointment.is_modifiable())


	def test_appointment_is_available(self):
		self.appointment.status = Appointment.Status.PENDING
		self.appointment.save()
		self.assertTrue(self.appointment.is_available())

		self.appointment.status = Appointment.Status.RESCHEDULING
		self.appointment.save()
		self.assertTrue(self.appointment.is_available())
