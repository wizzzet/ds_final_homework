from rest_framework import serializers


class JWTTokenResponseSerializer(serializers.Serializer):
    """
    Сериализатор возвращающий JWT токен
    """
    token = serializers.CharField()


class RecoveryTokenResponseSerializer(serializers.Serializer):
    """
    Сериализатор ответа содержащий хеш восстановления пароля
    """
    token = serializers.CharField(min_length=50, max_length=50)


class SuccessResponseSerializer(serializers.Serializer):
    """
    Сериализатор успешного ответа
    """
    status = serializers.CharField()
    detail = serializers.CharField(required=False)


class ErrorSerializer(serializers.Serializer):
    code = serializers.CharField()
    message = serializers.CharField()
    name = serializers.CharField()


class ErrorDetailSerializer(serializers.Serializer):
    errors = ErrorSerializer(many=True)


class ValidationErrorResponseSerializer(serializers.Serializer):
    """
    Сериализатор ответа с ошибками валидации
    """
    status = serializers.CharField()
    detail = ErrorDetailSerializer(required=False)
