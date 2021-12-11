import os
import sys

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

this_file_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.join(this_file_dir, '..'))
sys.path.insert(0, os.path.join(this_file_dir, '../apps'))
sys.path.insert(0, this_file_dir)

app = Celery('project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
