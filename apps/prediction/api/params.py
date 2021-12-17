from drf_yasg import openapi

query_param = openapi.Parameter(
    'query',
    openapi.IN_QUERY,
    description='Выражение запроса',
    type=openapi.TYPE_STRING
)
