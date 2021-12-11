import datetime

import pytz
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import utc


def local_to_utc(dt):
    if dt is None:
        return None

    tz = pytz.timezone(settings.TIME_ZONE)

    utc_dt = dt - tz.utcoffset(dt)
    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=utc)
    return utc_dt


def utcnow():
    return datetime.datetime.utcnow().replace(tzinfo=utc)


def local_now(date_format=True):
    now = timezone.localtime(timezone.now())

    if date_format:
        return now.strftime('%d.%m.%Y %H:%M:%S')

    return now
