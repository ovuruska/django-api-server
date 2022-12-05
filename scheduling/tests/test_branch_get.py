from django.test import TestCase

from scheduling.models import Branch

test_branches = [
	{
		'name': 'Branch 1',
		'address': 'Address 1',
		'description': 'Description 1',
		'tubs': 1,
	},
	{
		'name': 'Branch 2',
		'address': 'Address 2',
		'description': 'Description 2',
		'tubs': 2,
	},
]


class AppointmentTestCase(TestCase):

	def setUp(self) -> None:
		Branch.objects.create(name="branch1", address="address1", description="description1", tubs=1)
		Branch.objects.create(name="branch2", address="address2", description="description2", tubs=2)


	def test_list_branches(self):
		results = self.client.get('/api/branch/all')
		self.assertEqual(results.status_code, 200)
		self.assertEqual(len(results.json()), 2)

	def test_retrieve_branch(self):
		result = self.client.get('/api/branch/qwerqwer')
		self.assertEqual(result.status_code, 200)
		self.assertEqual(len(result.json()), 0)

		pk = Branch.objects.get(name="branch1").pk
		result = self.client.get(f'/api/branch/{pk}')
		self.assertEqual(result.status_code, 200)
		self.assertEqual(len(result.json()), 1)
		self.assertEqual(result.json()[0]['name'], "branch1")
		self.assertEqual(result.json()[0]['address'], "address1")
		self.assertEqual(result.json()[0]['description'], "description1")
		self.assertEqual(result.json()[0]['tubs'], 1)


