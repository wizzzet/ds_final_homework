from django.core.management.base import BaseCommand
from exchange import services


class Command(BaseCommand):
    """Выгрузка предложений в CSV"""

    help = 'Выгрузка предложений в CSV'

    def handle(self, *args, **options):
        services.export_passages()
