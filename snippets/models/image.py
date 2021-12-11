from django.conf import settings
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.utils.html import format_html
from easy_thumbnails.exceptions import (EasyThumbnailsError,
                                        InvalidImageFormatError)
from easy_thumbnails.files import get_thumbnailer


class ImageMixin(models.Model):
    standard_image = format_html(
        f'<img src="{settings.MEDIA_URL}images/blank.gif" '
        'alt="" style="width:50px;height:40px;" />'
    )
    image_field = 'image'
    image_size = (70, 40)

    def image_thumb(self):
        image = getattr(self, self.image_field)
        if image and not isinstance(image, ImageFieldFile):
            return format_html(
                f'<img src="{image.url}" alt="" '
                f'style="max-width:{self.image_size[0]}px;'
                f'max-height:{self.image_size[1]}px;">'
            )
        else:
            try:
                return format_html(
                    '<img src="%s" alt="" />' % get_thumbnailer(
                        getattr(self, self.image_field)
                    ).get_thumbnail({
                        'size': self.image_size,
                        'detail': True,
                    }).url if image
                    else f'<img src="{settings.STATIC_URL}images/blank.gif" '
                         f'alt="" '
                         f'style="max-width:{self.image_size[0]}px;'
                         f'max-height:{self.image_size[1]}px;" />'
                )
            except (OSError, EasyThumbnailsError):
                return ''

    image_thumb.short_description = 'Изображение'

    def image_img(self, field='image'):
        try:
            if getattr(self, field, None):
                return format_html(
                    '<img src="%s" alt="" />' % get_thumbnailer(
                        getattr(self, field)
                    ).get_thumbnail({
                        'size': (0, 40),
                        'detail': True
                    }).url
                )
        except InvalidImageFormatError:
            return self.standard_image
        return self.standard_image

    def preview(self, field='image'):
        image = getattr(self, field, '')
        if image:
            return get_thumbnailer(image).get_thumbnail({
                'size': (78, 78),
                'detail': True,
                'background': '#FFFFFF'
            }).url
        return ''

    class Meta:
        abstract = True
