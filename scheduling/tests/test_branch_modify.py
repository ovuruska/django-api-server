from django.test import TestCase

from scheduling.models import Branch

from mock.branches import branches as test_branches





class AppointmentTestCase(TestCase):

	def setUp(self) -> None:
		Branch.objects.create(name="branch1", address="address1", description="description1", tubs=1)
		Branch.objects.create(name="branch2", address="address2", description="description2", tubs=2)


	def test_create_branch(self):
		results = self.client.post()
		self.assertEqual(results.status_code, 201)

		results = self.client.post()
		self.assertEqual(results.status_code, 201)

	def get_branches(self):
		# self.client.get('api/branch')
		...

	def test_modify_remove(self):

		...