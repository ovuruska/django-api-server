import json
import os
from typing import Union

import requests
import uuid
from dotenv import load_dotenv, find_dotenv
from payment.serializers.requests.create_credit_card import AddressSerializer


class CloverService:
	base_url = 'https://apisandbox.dev.clover.com/v1'

	def __init__(self, access_token = None):
		if access_token is None:
			_ = load_dotenv(find_dotenv())
			self.access_token = os.getenv('ACCESS_TOKEN')
		else:
			self.access_token = access_token
		self.api_key = self.get_api_key()

	def get_api_key(self):
		pakms_url = f"https://apisandbox.dev.clover.com/pakms/apikey"
		pakms_headers = {"Accept": "application/json", "Authorization": f"Bearer {self.access_token}"}
		response = requests.get(pakms_url, headers=pakms_headers)
		pakms_body = response.json()
		api_access_key = pakms_body["apiAccessKey"]
		return api_access_key

	def create_credit_card(self, card_number: str, brand: str, exp_month: str, exp_year: str, cvv: str, first_name: str,
	                       last_name: str, email: str, address: {"city":str, "country":str, "address_line_1":str, "address_line_2":str, "postal_code":str, "state":str}):
		tokens_url = "https://token-sandbox.dev.clover.com/v1/tokens"
		tokens_headers = {"Accept": "application/json", "apikey": self.api_key, "Content-Type": "application/json"}

		card_info = {"number": card_number, "exp_month": exp_month, "exp_year": exp_year, "cvv": cvv, "brand": brand}

		card_data = {"card": card_info}

		response = requests.post(tokens_url, headers=tokens_headers, json=card_data)
		# Throw 400 if card is invalid
		response.raise_for_status()
		tokenized_card = response.json()
		card_token_id = tokenized_card["id"]
		card_data = {**tokenized_card["card"]}
		body = {
			'firstName': first_name,
			'lastName': last_name,
			'email': email,
			'source': card_token_id,
			"shipping": {"address": {"city": address.get("city",""), "country": address.get("country",""),
			                         "line1": address.get("address_line_1",""), "line2":address.get("address_line_2",""), "postal_code": address.get("postal_code",""),
			                         "state": address.get("state","")}}
		}

		base_url = 'https://scl-sandbox.dev.clover.com'
		endpoint = f'{base_url}/v1/customers'

		headers = {
			'Accept': 'application/json',
			'Content-Type': 'application/json',
			'Authorization': f'Bearer {self.access_token}',
		}
		response = requests.post(endpoint, headers=headers, json=body)
		customer_id = response.json()['id']
		return {
			'customer_token': customer_id,
			'card_token': card_token_id,
			**card_data,
		}

	def charge(self, amount, currency, source,idempotency_key:str,tip_amount=None):
		url = f'{self.base_url}/charges'
		headers = {'accept': 'application/json', 'authorization': f'Bearer {self.access_token}',
			'idempotency-key': idempotency_key, 'content-type': 'application/json'}
		data = {'amount': amount, 'currency': currency, 'source': source, }
		if tip_amount:
			data['tip_amount'] = tip_amount

		response = requests.post(url, headers=headers, json=data)
		response.raise_for_status()
		return response.json()

	def delete_credit_card(self,customer_token : str, card_token : str):
		return None

