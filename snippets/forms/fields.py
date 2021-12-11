import six
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from django.forms import FileField, ImageField
from PIL import Image

from snippets.forms import validators
from snippets.forms.widgets import MultipleFileInput


class MultipleFileField(FileField):
    widget = MultipleFileInput
    empty_values = list(EMPTY_VALUES)

    def to_python(self, data):
        if data in self.empty_values:
            return None
        for data_item in data:
            self.data_item_to_python(data_item)
        return data

    def data_item_to_python(self, data):
        if data is None:
            return None

        try:
            file_name = data.name
            file_size = data.size
        except AttributeError:
            raise ValidationError(
                self.error_messages['invalid'], code='invalid'
            )

        if self.max_length is not None and len(file_name) > self.max_length:
            params = {
                'max': self.max_length,
                'length': len(file_name),
            }
            raise ValidationError(
                self.error_messages['max_length'], code='max_length',
                params=params
            )

        if not file_name:
            raise ValidationError(
                self.error_messages['invalid'], code='invalid'
            )

        if not self.allow_empty_file and not file_size:
            raise ValidationError(self.error_messages['empty'], code='empty')

        return data


class MultipleImageField(MultipleFileField, ImageField):
    default_validators = [validators.validate_image_file_extension_multiple]

    def data_item_to_python(self, data):
        """
        Checks that uploaded data contains a valid image
        (GIF, JPG, PNG or whatever the PIL supports)
        See ImageField at
        https://github.com/django/django/blob/stable/1.5.x/django/forms/
        fields.py for details
        """
        data = super(MultipleImageField, self).data_item_to_python(data)

        # PIL is required to verify file

        if hasattr(data, 'temporary_file_path'):
            data_file = data.temporary_file_path()
        else:
            if hasattr(data, 'read'):
                data_file = six.BytesIO(data.read())
            else:
                data_file = six.BytesIO(data['content'])

        try:
            # Image.verify() must be called immediately after the constructor
            Image.open(data_file).verify()
        except Exception:
            raise ValidationError(self.error_messages['invalid_image'])

        if hasattr(data, 'seek') and callable(data.seek):
            data.seek(0)

        return data
