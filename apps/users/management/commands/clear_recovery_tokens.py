from django.core.management.base import BaseCommand
from users import models

from snippets.utils.datetime import utcnow


class Command(BaseCommand):
    def handle(self, *args, **options):
        now = utcnow()
        base_qs = models.User.objects.all()

        restore_salt_cnt = base_qs.filter(
            restore_salt__isnull=False, restore_salt_expiry__lt=now
        ).update(
            restore_salt_expiry=None, restore_salt=None
        )
        print('Expired recovery salts removed: %s' % restore_salt_cnt)

        restore_token_cnt = base_qs.filter(
            restore_token__isnull=False, restore_token_expiry__lt=now
        ).update(
            restore_token_expiry=None, restore_token=None
        )
        print('Expired recovery hashes removed: %s' % restore_token_cnt)
