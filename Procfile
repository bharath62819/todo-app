web: gunicorn todo.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn todo.wsgi