from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from faker import Faker
from knox.models import AuthToken

from common.roles import Roles
from scheduling.models import Employee, Appointment, Dog, Customer, Branch, Service, Product


class AuthTestCase(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.employee = Employee.objects.create(name='John Doe', email='john@example.com', role=Roles.EMPLOYEE_FULL_GROOMING)
        self.user = User.objects.create_user(
            username = 'testuser',
            password='testpassword'
        )
        self.employee.user = self.user
        self.employee.save()
        # Login
        self.token_instance, self.token = AuthToken.objects.create(self.user)
        self.headers = {'HTTP_AUTHORIZATION': f'Token {self.token}'}

        fake = Faker()

        self.customer = Customer.objects.create(name='John Doe', email='john.doe@example.com')
        self.dog = Dog.objects.create(name='Fido', breed='Golden Retriever', owner=self.customer)
        self.branch = Branch.objects.create(name='Main Branch', address='123 Main St')
        # duration = models.DurationField()

        self.service = Service.objects.create(name='Bath', description='Dog bath service', cost=25.0,
                                              duration=fake.time_delta())

        self.product = Product.objects.create(name='Shampoo', description='Dog shampoo', cost=10.0)
        self.appointment = Appointment.objects.create(customer=self.customer, dog=self.dog, start=timezone.now(),
                                                      end=timezone.now(), branch=self.branch, employee=self.employee, )
        self.appointment.services.add(self.service)
        self.appointment.products.add(self.product)
        self.appointment.save()


class TestAppointmentAvailableHoursAPIView(AuthTestCase):

    def test_appointment_available_hours_view(self):
        # Retrieve
        response = self.client.get(
            f'/api/branch/{self.branch.id}/free_hours',
            **self.headers
        )
        self.assertEqual(response.status_code, 200)
