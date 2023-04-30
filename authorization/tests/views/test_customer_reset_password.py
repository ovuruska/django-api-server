from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from scheduling.models import Customer

User = get_user_model()


class CustomerResetPasswordAPIViewTestCase(TestCase):
	queryset = Customer.objects.all()
	def setUp(self):
		self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

	#@patch('authorization.views.customer.MailChimp')
	def test_send_password_reset_email(self):
		pass
		# Set up the mock MailChimp client

		"""
		
	
		mock_client = mock_mailchimp.return_value
		mock_client.lists.members.create.return_value = {'status': 'subscribed'}
	
		# Send a POST request to the view with the user's email
		response = self.client.post(reverse('customer-reset-password'), data={'email': self.user.email})
	
		# Check that the response is successful
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content.decode(), f'Password reset email sent to {self.user.email}')
	
		# Check that the MailChimp client was called with the correct arguments
		mock_mailchimp.assert_called_once_with(mc_api='cb0a4190cb9430ce9c08ffad42faa6fe-us9', mc_user='Quicker MailChimp')
		mock_client.lists.members.create.assert_called_once()
		args, kwargs = mock_client.lists.members.create.call_args
		self.assertEqual(args[0], 'YOUR_LIST_ID')
		self.assertEqual(kwargs['data']['email_address'], self.user.email)
		self.assertEqual(kwargs['data']['status'], 'subscribed')
		self.assertIn('PASSWORD_RESET_LINK', kwargs['data']['merge_fields'])
		"""
