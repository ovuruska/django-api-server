from django.test import TestCase

from common import Mock


class TestMockGenerator(TestCase):

	def test_mock_generator(self):
		"""
			Tests the mock generator
		"""
		generator = Mock()
		generator.generate()