from django.core.management.base import BaseCommand
from exchange import services


class Command(BaseCommand):
    """Импорт записей StackExchange"""

    help = 'Импорт записей StackExchange'

    def add_arguments(self, parser):
        parser.add_argument('site', type=str)
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        services.import_posts(options['site'], options['path'])
