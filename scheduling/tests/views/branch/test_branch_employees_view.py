from django.test import TestCase
from django.contrib.auth.models import User
from knox.models import AuthToken

from common.roles import Roles
from scheduling.models import Employee, Branch


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
        self.branch = Branch.objects.create(name='Main Branch', address='123 Main St')
        self.branch.save()

class TestBranchEmplloyeesAPIView(AuthTestCase):

        def test_branch_employees_view(self):
            response = self.client.get(f'/api/branch/{self.branch.id}/employees?date=2025-12-28', **self.headers)
            self.assertEqual(response.status_code, 200)