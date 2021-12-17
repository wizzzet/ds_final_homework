from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'prediction'
    verbose_name = 'Прогнозирование'
