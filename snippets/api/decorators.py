from snippets.api.response import error_response


def public(func):
    func.is_public_http_method = True
    return func


def authenticated_should_not_pass(api_method, http_status=403):
    def wrapper(handler, request, *args, **kwargs):
        # запрещаем для уже вошедших
        if request.user.is_authenticated():
            return error_response(
                'Вы уже вошли в систему, регистрация невозможна',
                status=http_status,
                code='already_logged_in'
            )
        return api_method(handler, request, *args, **kwargs)
    return wrapper
