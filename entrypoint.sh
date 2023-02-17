#!/bin/bash

# Run the Django migrations
python manage.py migrate

# Generate the initial values using the mock script
python manage.py shell -c "from common import mock; m = mock.Mock(); m.generate()"

# Start the Django development server
python manage.py runserver 0.0.0.0:80
