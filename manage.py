#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import firebase_admin


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrubbers_backend.settings')
    try:
        from django.core.management import execute_from_command_line
        dirname = os.path.dirname(os.path.abspath(__file__))
        credentials = firebase_admin.credentials.Certificate(os.path.join(dirname,"firebase-config.json"))
        firebase_admin.initialize_app(credentials)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
