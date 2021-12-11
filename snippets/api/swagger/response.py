from drf_yasg.openapi import Response as OpenApiResponse

from snippets.api.swagger import serializers

jwt_token_response = OpenApiResponse(
    'Ответ содержащий JWT токен',
    serializers.JWTTokenResponseSerializer
)


recovery_token_response = OpenApiResponse(
    'Ответ содержащий хеш для восстановления пароля',
    serializers.RecoveryTokenResponseSerializer
)


success_response = OpenApiResponse(
    'Успешный ответ',
    serializers.SuccessResponseSerializer
)


validation_error_response = OpenApiResponse(
    'Ответ с ошибками валидации',
    serializers.ValidationErrorResponseSerializer
)
