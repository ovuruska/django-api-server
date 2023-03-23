from django.test import TestCase

from django.contrib.auth.models import User

from common.roles import Roles
from scheduling.models import Employee


class EmployeeModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='johndoe', password='testpassword')

        self.employee = Employee.objects.create(
            name='John Doe',
            uid='1234567890',
            email='john.doe@example.com',
            phone='123-456-7890',
            branch=None,
            user=self.user,
            role=Roles.EMPLOYEE_WE_WASH,
        )

    def test_employee_creation(self):
        self.assertIsNotNone(self.employee)
        self.assertEqual(self.employee.name, 'John Doe')
        self.assertEqual(self.employee.uid, '1234567890')
        self.assertEqual(self.employee.email, 'john.doe@example.com')
        self.assertEqual(self.employee.phone, '123-456-7890')
        self.assertEqual(self.employee.user, self.user)
        self.assertEqual(self.employee.role, Roles.EMPLOYEE_WE_WASH)


    def test_employee_deletion(self):
        self.employee.delete()
        self.assertEqual(Employee.objects.count(), 0)


