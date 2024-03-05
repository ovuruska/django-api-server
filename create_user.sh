# Export all inside .env
cat .env | bash
rm -rf db.sqlite3 && python3 manage.py migrate && python3 manage.py add_admin
