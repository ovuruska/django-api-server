from django.test import TestCase

from scheduling.models import Branch

"""
This tests suite contains a single tests case:

test_branch_creation: Tests whether the Branch instance is created correctly with the given data.

"""


class BranchModelTestCase(TestCase):
	def setUp(self):
		self.branch = Branch.objects.create(
			name='Main Branch',
			address='123 Main St',
			description='The main branch of our store',
			phone='123-456-7890',
			email='main.branch@example.com',
			tubs=5
		)

	def test_branch_creation(self):
		self.assertIsNotNone(self.branch)
		self.assertEqual(self.branch.name, 'Main Branch')
		self.assertEqual(self.branch.address, '123 Main St')
		self.assertEqual(self.branch.description, 'The main branch of our store')
		self.assertEqual(self.branch.phone, '123-456-7890')
		self.assertEqual(self.branch.email, 'main.branch@example.com')
		self.assertEqual(self.branch.tubs, 5)

	def test_branch_deletion(self):
		self.branch.delete()
		self.assertEqual(Branch.objects.count(), 0)
