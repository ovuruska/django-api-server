from django.test import TestCase
from django.contrib.auth.models import User
from docutils.nodes import status
from knox.models import AuthToken

from common.roles import Roles
from scheduling.models import Employee, Customer, Branch


class AuthTestCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.employee = Employee.objects.create(name='John Doe', email='john@example.com', role=Roles.EMPLOYEE_FULL_GROOMING)
        self.user = User.objects.create_user(
            username = 'testuser',
            password='testpassword'
        )
        self.customer_user = User.objects.create_user(
            username='testcustomer',
            password='testpassword'
        )
        self.customer = Customer.objects.create(
            name='John Doe',
            uid='123456789',
        )
        self.customer.user = self.customer_user
        self.customer.save()
        self.employee.user = self.user
        self.employee.save()
        # Login
        self.token_instance, self.token = AuthToken.objects.create(self.customer.user)
        self.headers = {'HTTP_AUTHORIZATION': f'Token {self.token}'}

class TestSignedUrlRescheduleAPIView(AuthTestCase):
    def test_signed_url_reschedule_view(self):
        # Create a dog
        response = self.client.get(f'/api/confirmation/{self.token}/reschedule', **self.headers)
        self.assertEqual(response.status_code, 200)