#!/bin/bash
git pull
source venv/bin/activate
find . -type f -name "*.pyc" -exec rm -f {} \;
pip install -r requirements.txt
yes "yes" | python manage_admin.py migrate
python manage.py collectstatic --noinput
python manage_admin.py collectstatic --noinput
chown www-data:www-data -R .
touch venv/uwsgi.api.reload
touch venv/uwsgi.admin.reload
supervisorctl restart ds_celery
