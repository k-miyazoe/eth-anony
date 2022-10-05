python manage.py makemigrations

python manage.py migrate

# python manage.py runserver 0.0.0.0:9990

# uwsgi --socket :9990 --http :8001  --module config.wsgi --py-autoreload 1 -b 32768

# uwsgi --socket :4000 --module project.wsgi --py-autoreload 1 --logto /tmp/uwsgi.log

# python manage.py runserver 0.0.0.0:4000

gunicorn project.wsgi --bind=0.0.0.0:9990
