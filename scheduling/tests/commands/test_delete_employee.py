from django.core.management import call_command
from django.contrib.auth.models import User
from django.test import TestCase
from scheduling.models import Employee

"""
This tests suite contains three tests cases:

test_delete_employee_success: Tests whether the command successfully deletes both the User and the Employee instances for a given username.
test_delete_employee_user_does_not_exist: Tests whether the command raises a User.DoesNotExist exception when trying to delete a non-existing user.
"""

class DeleteEmployeeCommandTestCase(TestCase):
    def setUp(self):
        self.username = 'quicker-employee'
        self.user = User.objects.create_user(username=self.username, password='testpassword')
        self.employee = Employee.objects.create(user=self.user)

    def tearDown(self):
        User.objects.filter(username=self.username).delete()

    def test_delete_employee_success(self):
        call_command('delete_employee', self.username)
        self.assertFalse(User.objects.filter(username=self.username).exists())
        self.assertFalse(Employee.objects.filter(user=self.user).exists())

    def test_delete_employee_user_does_not_exist(self):
        non_existing_username = 'non_existing_user'
        call_command('delete_employee', non_existing_username)

