import os

import boto3
from dotenv import load_dotenv

EMAIL_ADDRESS="ovuruska@gmail.com"

def get_client(dotenv_path: str):
	load_dotenv(dotenv_path)
	aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
	aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
	aws_region = os.environ.get("AWS_REGION")

	ses_client = boto3.client("ses", region_name=aws_region, aws_access_key_id=aws_access_key_id,
	                          aws_secret_access_key=aws_secret_access_key)
	return ses_client


def send_email(to : str,title:str, body: str):
	dirpath = os.path.abspath(os.path.dirname(__file__))
	env_path = os.path.join(dirpath,"aws.env")
	ses_client = get_client(env_path)

	CHARSET = "UTF-8"

	response = ses_client.send_email(
		Destination={
			"ToAddresses": [
				to,
			],
		},
		Message={
			"Body": {
				"Text": {
					"Charset": CHARSET,
					"Data":body,
				}
			},
			"Subject": {
				"Charset": CHARSET,
				"Data": title,
			},
		},
		Source=EMAIL_ADDRESS,
	)
	return response
