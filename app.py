import os
import sys

from django.core.wsgi import get_wsgi_application

from serverless_wsgi import handle_request

# Set the path to the Django project
sys.path.insert(0, os.path.abspath("."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrubbers_backend.settings")

# Get the WSGI application
application = get_wsgi_application()


def handler(event, context):
	print("DB NAME: ",os.environ.get("DB_NAME", None))
	print("DB USER: ",os.environ.get("DB_USER", None))
	print("DB PASSWORD: ",os.environ.get("DB_PASSWORD", None))
	print("DB HOST: ",os.environ.get("DB_HOST", None))
	print("DB PORT: ",os.environ.get("DB_PORT", None))

	return handle_request(application, event, context)

