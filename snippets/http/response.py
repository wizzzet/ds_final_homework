from django.http import JsonResponse
from rest_framework.response import Response


def error_response(message=None, status=400, code=None, only_json=False):
    result = {
        'status': 'error'
    }
    if message is not None:
        result['detail'] = message

    if code:
        result['code'] = code

    if only_json:
        return JsonResponse(result, status=status)

    return Response(result, status=status)


def success_response(message=None, status=200):
    result = {
        'status': 'ok'
    }
    if message is not None:
        result['detail'] = message
    return Response(result, status=status)


def validation_error_response(errors, status=400, code=None):
    return error_response(message={'errors': errors}, status=status, code=code)
