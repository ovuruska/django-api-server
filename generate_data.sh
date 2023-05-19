export DB_HOST=localhost
rm -rf db.sqlite3 && python manage.py migrate && python manage.py generate_data 100
