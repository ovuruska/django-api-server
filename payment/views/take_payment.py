from rest_framework.views import APIView
import requests
from dotenv import load_dotenv, find_dotenv
import os
_ = load_dotenv(find_dotenv())

client_secret = os.getenv('CLIENT_SECRET')
client_id = os.getenv('CLIENT_ID')
merchant_id = os.getenv('MERCHANT_ID')




class TakePaymentView(APIView):
	def get_token_endpoint(self, client_id, client_secret, authorization_code):
		return f"https://sandbox.dev.clover.com/oauth/token?client_id={client_id}&client_secret={client_secret}&code={authorization_code}&grant_type=authorization_code"

	def post(self, request, *args, **kwargs):
		authorization_code = request.data.get('authorization_code')
		response = requests.get(self.get_token_endpoint(client_id, client_secret, authorization_code))
		body = response.json()
		access_token = body['access_token']
		api_access_key = self.get_api_access_key(access_token)


	def get_api_access_key(self,access_token):
		pakms_url = f"https://apisandbox.dev.clover.com/pakms/apikey"
		pakms_headers = {
			"Accept": "application/json",
			"Authorization": f"Bearer {access_token}"
		}
		response = requests.get(pakms_url, headers=pakms_headers)
		body = response.json()
		return body['apiAccessKey']


