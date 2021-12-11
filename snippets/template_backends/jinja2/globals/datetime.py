import time

from django.conf import settings
from django.utils import formats
from django.utils.dateformat import format as date_format
from django.utils.timezone import template_localtime

from snippets.template_backends.jinja2 import jinjafilter


@jinjafilter
def date(value, arg, use_l10n=True):
    value = template_localtime(value)
    if value in (None, ''):
        return ''
    if arg is None:
        arg = settings.DATE_FORMAT
    if arg == 'timestamp':
        return str(int(time.mktime(value.timetuple())))
    try:
        return formats.date_format(value, arg, use_l10n=use_l10n)
    except AttributeError:
        try:
            return date_format(value, arg)
        except AttributeError:
            return ''
