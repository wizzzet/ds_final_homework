from typing import Dict

from django.conf import settings
from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors import FieldInspector, SwaggerAutoSchema


class ProjectSwaggerAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        tags = super().get_tags(operation_keys)

        if 'api' in tags and operation_keys:
            tags[0] = operation_keys[1]
        return tags


class SimpleInspector(FieldInspector):
    """
    FieldInspector, удаляющий поля title & minLength из схемы
    """
    def process_result(self, result, method_name, obj, **kwargs):

        if isinstance(result, openapi.Schema.OR_REF):
            schema = openapi.resolve_ref(result, self.components)
            schema.pop('title', None)
            schema.pop('minLength', None)

        return result


class SimpleAutoSchema(SwaggerAutoSchema):
    """
    Простая схема по-умолчанию, без атрибутов title & minLength
    """
    field_inspectors = [
        SimpleInspector
    ] + swagger_settings.DEFAULT_FIELD_INSPECTORS


version_param = openapi.Parameter(
    'version',
    openapi.IN_PATH,
    description='Версия API',
    type=openapi.TYPE_STRING,
    default=settings.API_CURRENT_VERSION
)


def common_openapi_params(*params) -> Dict:
    manual_parameters = [version_param]
    manual_parameters.extend(params)
    return {
        'manual_parameters': manual_parameters
    }
