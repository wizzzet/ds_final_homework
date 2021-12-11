from django.db import models
from solo.models import SingletonModel

from snippets.models.abstract import BaseModel
from snippets.models.seo import SEOModelMixin


class BasePage(SEOModelMixin, SingletonModel, BaseModel):
    """Базовая модель страниц"""

    title = models.CharField(
        'Заголовок', max_length=255, blank=True, null=True
    )

    translation_fields = SEOModelMixin.translation_fields + ('title',)

    class Meta:
        abstract = True

    def __str__(self):
        return self._meta.verbose_name
