import json

import requests
from django.test import TestCase

FIREBASE_WEB_API_KEY = "AIzaSyBAxjf_H7Uh_PV2a5qu5oKWKSp408hlFH0"
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
email = "abc@test.com"
password = "12341234"

def sign_in_with_email_and_password(email: str, password: str, return_secure_token: bool = True):
	payload = json.dumps({
		"email": email,
		"password": password,
		"returnSecureToken": return_secure_token
	})

	r = requests.post(rest_api_url,
	                  params={"key": FIREBASE_WEB_API_KEY},
	                  data=payload)

	return r.json()

"""
class FirebaseAuthTestCase(TestCase):

	def test_sign_in_with_email_and_password(self):
		response = sign_in_with_email_and_password(email,password)
		user_id = response.get("localId")
		id_token = response.get("idToken")
		result = self.client.get(f"/api/me/{user_id}",HTTP_AUTHORIZATION=f"Bearer {id_token}")

	def test_sign_in_with_email_and_password_invalid(self):
		try:
			result = self.client.get(f"/api/me/123",HTTP_AUTHORIZATION=f"Bearer 123")
			raise AssertionError("Should have thrown an exception")
		except Exception as e:
			...
"""
