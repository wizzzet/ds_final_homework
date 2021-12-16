from django.core.management.base import BaseCommand
from exchange import services


class Command(BaseCommand):
    """Обновление наиболее подходящих ответов"""

    help = 'Обновление наиболее подходящих ответов'

    def handle(self, *args, **options):
        services.update_most_voted_answers()
