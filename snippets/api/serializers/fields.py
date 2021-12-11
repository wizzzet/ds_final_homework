from django.conf import settings
from django.template import defaultfilters as filters
from django.template.defaultfilters import urlencode
from rest_framework import serializers

from snippets.enums import StatusEnum
from snippets.template_backends.jinja2.globals import (cropped_thumbnail,
                                                       thumbnail)

__all__ = (
    'CroppingThumbnailField', 'FileField', 'ImageField', 'ImageMetaField',
    'PublishedRelationField', 'PretextField', 'ThumbnailField'
)


class CroppingThumbnailField(serializers.Field):
    def __init__(self, **kwargs):
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        cropping_parameters = kwargs.pop('cropping_parameters', {})
        self.cropping_parameters = cropping_parameters
        super(CroppingThumbnailField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        result = cropped_thumbnail(
            value, self.field_name, **self.cropping_parameters
        )
        if result:
            return '%s%s' % (settings.MEDIA_URL, result)


class FileField(serializers.FileField):
    def to_representation(self, value):
        result = super(FileField, self).to_representation(value)
        if result:
            return '%s%s' % (settings.MEDIA_URL, urlencode(result))


class ImageField(serializers.ImageField):
    def to_representation(self, value):
        result = super(ImageField, self).to_representation(value)
        if result:
            return f'{settings.MEDIA_URL}{urlencode(result)}'


class ImageMetaField(serializers.ImageField):
    def to_representation(self, value):
        url = super(ImageMetaField, self).to_representation(value)
        if url:
            url = f'{settings.MEDIA_URL}{urlencode(url)}'

        return {
            'height': value.height,
            'width': value.width,
            'url': url
        }


class PretextField(serializers.ReadOnlyField):
    def to_representation(self, value):
        result = super(PretextField, self).to_representation(value)
        if result:
            return filters.linebreaksbr(result)


class PublishedRelationField(serializers.Field):
    """"""
    def __init__(self, serializer_class, many=True, **kwargs):
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        self.filters = kwargs.pop('filters', None)
        self.select_related = kwargs.pop('select_related', None)
        self.serializer_class = serializer_class
        # булевое поле, отвечающее за отображение
        self.show_field = kwargs.pop('show_field', None)
        self.many = many
        super(PublishedRelationField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        if self.show_field is not None:
            if not getattr(value, self.show_field):
                if self.many:
                    return []
                return None

        qs = None
        if self.many:
            qs = getattr(value, self.field_name).published()
            if self.filters:
                qs = qs.filter(self.filters)

            if self.select_related:
                qs = qs.select_related(*self.select_related)
        else:
            obj = getattr(value, self.field_name)
            if obj and obj.status == StatusEnum.PUBLIC:
                qs = obj

        if qs:
            return self.serializer_class(qs, many=self.many).data

        return [] if self.many else None


class ThumbnailField(serializers.Field):
    def __init__(self, thumbnail_parameters=None, image_field=None, **kwargs):
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        self.thumbnail_parameters = thumbnail_parameters or {}
        self.image_field = image_field
        super(ThumbnailField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        field = self.image_field if self.image_field else self.field_name
        if hasattr(value, field) and getattr(value, field):
            result = thumbnail(
                getattr(value, field), **self.thumbnail_parameters
            )
            return result if result else None

        return None
