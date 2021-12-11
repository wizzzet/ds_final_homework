from django.db import models


class SEOModelMixin(models.Model):
    """SEO миксин"""
    seo_title = models.CharField(
        'META заголовок (title)', blank=True, null=True, max_length=255
    )
    seo_description = models.TextField(
        'META описание (description)', blank=True, null=True,
        max_length=1024
    )

    translation_fields = ('seo_title', 'seo_description')

    class Meta:
        abstract = True
