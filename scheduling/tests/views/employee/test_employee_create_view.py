from django.test import TestCase
from django.contrib.auth.models import User
from knox.models import AuthToken

from common.roles import Roles
from scheduling.models import Employee

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


class TestEmployeeCreateAPIView(AuthTestCase):

    def test_employee_create_view(self):
        response = self.client.post('/api/employee', data={
            "name": "John Doe",
            "uid": "1234567890",
            "email" : "john.doe@example.com",
            "phone": "123-456-7890"
            }, **self.headers)
        role = Roles.EMPLOYEE_WE_WASH,
        self.assertEqual(response.status_code, 201)
