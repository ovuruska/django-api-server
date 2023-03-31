from io import StringIO
from unittest.mock import patch
from django.core.management import call_command
from django.contrib.auth.models import User
from django.test import TestCase
from scheduling.models import Customer


"""
This tests suite contains a single tests case:

test_add_customer_success: Tests whether the command successfully creates a new User and Customer instance with the given input.
To tests the user input, we use the unittest.mock.patch context manager to mock the input function. In this tests, the input function will return the values stored in self.username, self.password, and self.email when called.
"""
class AddCustomerCommandTestCase(TestCase):
    def setUp(self):
        self.username = 'new-customer'
        self.password = 'testpassword'
        self.email = 'new-customer@example.com'

    def tearDown(self):
        User.objects.filter(username=self.username).delete()

    def test_add_customer_success(self):
        with patch('builtins.input', side_effect=[self.username, self.password, self.email]):
            call_command('add_customer')

        user = User.objects.get(username=self.username)
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password(self.password))
        self.assertEqual(user.email, self.email)

        customer = Customer.objects.get(user=user)
        self.assertIsNotNone(customer)
        self.assertEqual(customer.email, self.email)