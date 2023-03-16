from unittest.mock import patch
from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth.models import User
from scheduling.models import Customer

class AddCustomerCommandTestCase(TestCase):
    def setUp(self):
        self.username = "test_customer"
        self.password = "test_password"
        self.email = "test_customer@example.com"

    def test_add_customer_command(self):
        with patch('builtins.input', side_effect=[self.username, self.password, self.email]):
            call_command("add_customer")

        # check if customer is added in database
        customer = User.objects.get(username=self.username)
        self.assertEqual(customer.email, self.email)

        customer_detail = Customer.objects.get(user=customer)
        self.assertEqual(customer_detail.email, self.email)

    def tearDown(self):
        try:
            customer = User.objects.get(username=self.username)
            customer.delete()
        except User.DoesNotExist:
            pass