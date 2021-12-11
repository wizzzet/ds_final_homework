from project.celery_app import app as celery_app

default_app_config = 'project.apps.AppConfig'

__all__ = ('celery_app',)
