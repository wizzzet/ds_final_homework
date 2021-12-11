from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors import FieldInspector, SwaggerAutoSchema


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
