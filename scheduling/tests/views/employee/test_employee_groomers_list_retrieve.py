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

class EmployeeGroomerListRetrieveTestCase(AuthTestCase):


    def test_employee_groomer_list_retrieve(self):
        # make the request
        response = self.client.get('/api/employee/groomers',**self.headers)

        # check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{'id': self.employee.id, 'name': 'John Doe', 'email': 'john@example.com'}])