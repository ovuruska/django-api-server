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

class EmployeeRetrieveModifyDestroyViewTest(AuthTestCase):

    def test_employee_retrieve_view(self):
        # Retrieve
        response = self.client.get(f'/api/employee/{self.employee.id}', **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_employee_modify_view(self):
        # Modify
        response = self.client.patch(
            f'/api/employee/{self.employee.id}',
            data={"name": "Jane Doe"},
            format='json',
            content_type='application/json',  # Add the Content-Type header
            **self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Employee.objects.get(id=self.employee.id).name, "Jane Doe")

    def test_employee_destroy_view(self):
        # Destroy
        response = self.client.delete(f'/api/employee/{self.employee.id}', **self.headers)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Employee.objects.count(), 0)


