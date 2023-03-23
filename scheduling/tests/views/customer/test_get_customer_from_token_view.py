from django.test import TestCase
from django.contrib.auth.models import User
from knox.models import AuthToken

from common.roles import Roles
from scheduling.models import Employee, Customer


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
        self.token_instance, self.token = AuthToken.objects.create(self.customer_user)
        self.headers = {'HTTP_AUTHORIZATION': f'Token {self.token}'}

class TestGetCustomerFromTokenAPIView(AuthTestCase):

        def test_get_customer_from_token_view(self):
            response = self.client.get('/api/me', **self.headers)
            self.assertEqual(response.status_code, 200)