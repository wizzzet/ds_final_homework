from django.db import models
from exchange.choices import StackExchangeSiteChoices

from snippets.models import BasicModel, LastModMixin


class StackExchangePost(LastModMixin, BasicModel):
    """Записи StackExchange"""

    id = models.BigAutoField('Id', primary_key=True)
    source_site = models.CharField(
        'Сайт', max_length=100, choices=StackExchangeSiteChoices.choices
    )
    source_id = models.BigIntegerField('Идентификатор источника')
    source_type = models.PositiveSmallIntegerField('Тип записи')
    source_parent_id = models.BigIntegerField(
        'Идентификатор родителя в источнике', blank=True, null=True
    )
    parent = models.ForeignKey(
        'self', verbose_name='Родительская запись', on_delete=models.SET_NULL,
        related_name='children', blank=True, null=True
    )
    score = models.IntegerField('Скоринг', blank=True, null=True)
    title = models.TextField('Заголовок', blank=True)
    title_cleaned = models.TextField('Заголовок очищенный', blank=True)
    body = models.TextField('Текст', blank=True)
    body_cleaned = models.TextField('Текст очищенный', blank=True, null=True)
    owner_user_id = models.BigIntegerField(
        'Идентификатор автора', blank=True, null=True
    )

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
    most_voted_answer = models.ForeignKey(
        'self', verbose_name='Самый популярный ответ', blank=True, null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        unique_together = ('source_site', 'source_id')
        verbose_name = 'Запись StackExchange'
        verbose_name_plural = 'Записи StackExchange'

    def __str__(self):
        return (
            self.title_cleaned or self.body_cleaned[:50] or str(self.source_id)
        )
