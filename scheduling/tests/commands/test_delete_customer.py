from django.core.management import call_command
from django.contrib.auth.models import User
from django.test import TestCase
from scheduling.models import Customer

"""
This tests suite contains three tests cases:

test_delete_customer_success: Tests whether the command successfully deletes both the User and the Customer instances for a given username.
test_delete_customer_user_does_not_exist: Tests whether the command raises a User.DoesNotExist exception when trying to delete a non-existing user.
test_delete_customer_no_customer_model: Tests whether the command successfully deletes the User instance even when there is no associated Customer instance.
To run the tests, simply use the python manage.py tests command along with the path to your tests file, like this:
"""
class DeleteCustomerCommandTestCase(TestCase):


    def setUp(self):
        self.username = 'quicker-customer'
        self.user = User.objects.create_user(username=self.username, password='testpassword')
        self.customer = Customer.objects.create(user=self.user)

    def tearDown(self):
        User.objects.filter(username=self.username).delete()

    def test_delete_customer_success(self):
        call_command('delete_customer', self.username)
        self.assertFalse(User.objects.filter(username=self.username).exists())
        self.assertFalse(Customer.objects.filter(user=self.user).exists())

    def test_delete_customer_user_does_not_exist(self):
        non_existing_username = 'non_existing_user'
        call_command('delete_customer', non_existing_username)


