from django.test import TestCase

from common import Mock


class MockTestCase(TestCase):
	def setUp(self) -> None:
		self.mock = Mock(number_of_appointments=500)
		self.data = self.mock.generate()

	def tearDown(self):
		self.mock.remove(self.data)