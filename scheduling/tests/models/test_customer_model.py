from django.contrib.auth.models import User
from django.test import TestCase
from common.roles import Roles
from scheduling.models import Customer

"""
This test suite contains two test cases:

test_customer_creation: Tests whether the Customer instance is created correctly with the given data.
test_customer_ordering: Tests the ordering of the Customer instances based on the name field.
"""

class CustomerModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='johndoe', password='testpassword')
        self.customer = Customer.objects.create(
            name='John Doe',
            uid='1234567890',
            email='john.doe@example.com',
            phone='123-456-7890',
            address='123 Main St',
            user=self.user,
            role=Roles.CUSTOMER,
            validated=True,
        )

    def test_customer_creation(self):
        self.assertIsNotNone(self.customer)
        self.assertEqual(self.customer.name, 'John Doe')
        self.assertEqual(self.customer.uid, '1234567890')
        self.assertEqual(self.customer.email, 'john.doe@example.com')
        self.assertEqual(self.customer.phone, '123-456-7890')
        self.assertEqual(self.customer.address, '123 Main St')
        self.assertEqual(self.customer.user, self.user)
        self.assertEqual(self.customer.role, Roles.CUSTOMER)
        self.assertTrue(self.customer.validated)

    def test_customer_ordering(self):
        customer2 = Customer.objects.create(
            name='Alice Smith',
            uid='9876543210',
            email='alice.smith@example.com',
            phone='321-654-0987',
            address='456 Main St',
            user=None,
            role=Roles.CUSTOMER,
            validated=True,
        )
        customers = Customer.objects.all()
        self.assertEqual(customers[0], customer2)
        self.assertEqual(customers[1], self.customer)
