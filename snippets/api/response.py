from django.conf import settings
from django.http import HttpResponse, JsonResponse
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED)


class Response(JsonResponse):
    def __init__(self, *args, **kwargs):
        kwargs['json_dumps_params'] = {'indent': 2} if settings.DEBUG else {}
        super(Response, self).__init__(*args, **kwargs)


class HttpResponseUnauthorized(HttpResponse):
    def __init__(self, *args, **kwargs):
        self.status_code = HTTP_401_UNAUTHORIZED
        super(HttpResponseUnauthorized, self).__init__(*args, **kwargs)


def error_response(message=None, status=HTTP_400_BAD_REQUEST, code=None):
    result = {
        'status': 'error',
        'detail': {}
    }

    if message is not None:
        if isinstance(message, (dict, list, tuple, set)):
            detail = message
        else:
            detail = {
                'errors': [{
                    'code': code,
                    'message': message,
                    'name': 'non_field_errors'
                }]
            }

        result['detail'] = detail

    return Response(result, status=status)


def success_response(message=None, status=HTTP_200_OK):
    result = {
        'status': 'ok'
    }
    if message is not None:
        result['detail'] = message
    return Response(result, status=status)


def validation_error_response(errors, status=HTTP_400_BAD_REQUEST, code=None):
    errors_list = []
    for name, errors in errors.items():

        for error in errors:
            errors_list.extend([{
                'message': str(error),
                'name': name,
                'code': error.code
            }])

    return error_response(
        message={'errors': errors_list}, status=status, code=code
    )


def not_authenticated_response(message=None, authentication_header=None):
    response = error_response(message=message, status=HTTP_401_UNAUTHORIZED)
    if authentication_header is not None:
        response['WWW-Authenticate'] = authentication_header

    return response
