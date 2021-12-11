from django.db import models
from exchange.choices import StackExchangeSiteChoices

from snippets.models import BasicModel, LastModMixin


class StackExchangePost(LastModMixin, BasicModel):
    """Записи StackExchange"""

    id = models.BigIntegerField('Id', primary_key=True)
    source_site = models.CharField(
        'Сайт', max_length=100, choices=StackExchangeSiteChoices.choices
    )
    source_id = models.BigIntegerField('Идентификатор источника')
    source_type = models.PositiveSmallIntegerField('Тип записи')
    source_parent_id = models.BigIntegerField('Идентификатор источника')
    parent = models.ForeignKey(
        'self', verbose_name='Родительская запись', on_delete=models.CASCADE,
        related_name='children'
    )
    score = models.IntegerField('Скоринг', blank=True, null=True)
    body = models.TextField('Текст', blank=True)
    body_cleaned = models.TextField('Текст очищенный', blank=True, null=True)
    owner_user_id = models.BigIntegerField('Идентификатор автора')

    source_created = models.DateTimeField(
        'Запись создана в источнике', blank=True, null=True
    )
    source_activity_date = models.DateTimeField(
        'Последняя активность в источнике', blank=True, null=True
    )
    last_trained = models.DateTimeField(
        'Использована в тренировке в предыдущий раз', blank=True, null=True
    )
    published = models.BooleanField('Опубликована', default=True)
    comments_count = models.IntegerField(
        'Количество комментариев', blank=True, null=True
    )

    class Meta:
        verbose_name = 'Запись StackExchange'
        verbose_name_plural = 'Записи StackExchange'
