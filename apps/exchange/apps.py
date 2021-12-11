from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'exchange'
    verbose_name = 'Синхронизация'
