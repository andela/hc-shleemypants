web: gunicorn hc.wsgi --log-file -
migrate ./manage.py migrate
ensuretriggers ./manage.py ensuretriggers
createsuperuser ./manage.py createsuperuser
