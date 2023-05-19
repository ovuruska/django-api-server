from collections import namedtuple
from requests import HTTPError
from payment.services.clover import CloverService
from django.urls import reverse
from unittest.mock import patch
from common.auth_test_case import CustomerAuthTestCase

CreditCardMock = namedtuple('CreditCard', ['customer_token', 'card_token', 'id',  'exp_month', 'exp_year', 'first6', 'last4', 'brand','cvv'])

class CreditCardWrapper:
    def __init__(self, credit_card):
        self.credit_card = credit_card

    def __getattr__(self, attr):
        return getattr(self.credit_card, attr)

    def delete(self):
        # Placeholder delete function
        pass

class DeleteCreditCardTestCase(CustomerAuthTestCase):
	credit_card_data = {
		'id':1,
		'exp_month': '01',
		'exp_year': '2025',
		'cvv': '123',
		'first6': '411111',
		'last4': '1111',
		'brand': 'VISA',
		'customer_token': "customer_1234",
		'card_token': "card_1234",
	}
	credit_card = CreditCardWrapper(CreditCardMock(**credit_card_data))

	@patch.object(CloverService, 'delete_credit_card')
	def test_delete_customer_credit_card(self,mock_delete_credit_card):
		with patch('payment.models.CreditCard.objects.get', return_value=self.credit_card) as mock_get:
				credit_card_id = self.credit_card.id
				url = reverse('payment/delete-card', kwargs={'pk': credit_card_id})
				with patch.object(self.credit_card, 'delete') as mock_delete:
					response = self.client.delete(url, **self.customer_headers)
					self.assertEqual(response.status_code, 204)
					mock_get.assert_called_once_with(id=credit_card_id, owner=self.customer)
					mock_delete_credit_card.assert_called_once_with(self.credit_card.customer_token, self.credit_card.card_token)
					mock_delete.assert_called_once()


	@patch.object(CloverService, 'delete_credit_card')
	def test_delete_customer_credit_card_not_found(self,mock_delete_credit_card):
		with patch('payment.models.CreditCard.objects.get', return_value=None) as mock_get:
				credit_card_id = 2
				url = reverse('payment/delete-card', kwargs={'pk': credit_card_id})
				with patch.object(self.credit_card, 'delete') as mock_delete:
					response = self.client.delete(url, **self.customer_headers)
					self.assertEqual(response.status_code, 404)
					mock_get.assert_called_once_with(id=credit_card_id, owner=self.customer)
					mock_delete_credit_card.assert_not_called()
					mock_delete.assert_not_called()
					response_data = response.json()
					self.assertEqual(response_data['detail'], f'Credit card with id {credit_card_id} not found')

	@patch.object(CloverService, 'delete_credit_card', side_effect=HTTPError('Test Exception'))
	def test_delete_customer_credit_card_exception(self,mock_delete_credit_card):
		with patch('payment.models.CreditCard.objects.get', return_value=self.credit_card) as mock_get:
				credit_card_id = self.credit_card.id
				url = reverse('payment/delete-card', kwargs={'pk': credit_card_id})
				with patch.object(self.credit_card, 'delete') as mock_delete:
					response = self.client.delete(url, **self.customer_headers)
					self.assertEqual(response.status_code, 503)
					mock_get.assert_called_once_with(id=credit_card_id, owner=self.customer)
					mock_delete_credit_card.assert_called_once_with(self.credit_card.customer_token, self.credit_card.card_token)
					mock_delete.assert_not_called()
					response_data = response.json()
					self.assertEqual(response_data['detail'], 'Test Exception')