from django.test import TestCase
from django.core.management import call_command


class GenerateMockDataCommandTestCase(TestCase):

	def test_generate_mock_data_with_scale(self):
		call_command('generate_data', scale=1)

	def test_generate_mock_data_with_interval(self):
		call_command('generate_data', scale=1, interval="1w")
