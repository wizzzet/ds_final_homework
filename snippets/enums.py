from collections import OrderedDict

from snippets.models import BaseEnumerate


class PaymentStatusEnum(BaseEnumerate):
    """ Статусы оплаты """
    NOT_PAID = -1
    PAID = 1

    values = OrderedDict((
        (NOT_PAID, 'Не оплачено'),
        (PAID, 'Оплачено')
    ))

    default = NOT_PAID


class StatusEnum(BaseEnumerate):
    """
    Object publicity status enumerate
    """
    DRAFT = 0
    PUBLIC = 1
    HIDDEN = 2

    values = OrderedDict((
        (DRAFT, 'Черновик'),
        (PUBLIC, 'Публичный'),
        (HIDDEN, 'Скрытый'),
    ))
