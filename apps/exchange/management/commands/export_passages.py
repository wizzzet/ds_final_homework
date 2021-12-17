from django.core.management.base import BaseCommand
from exchange import services


class Command(BaseCommand):
    """Выгрузка предложений в CSV"""

    help = 'Выгрузка предложений в CSV'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        services.export_passages(options.get('path'))
