from django.conf import settings
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

from snippets.api.response import error_response


class LanguageMiddleware(MiddlewareMixin):
    """Language middleware"""
    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs):

        lang = (
            view_kwargs.get('lang')
            or translation.get_language_from_request(request, check_path=False)
            or settings.DEFAULT_LANGUAGE
        ).lower()

        available_langs = settings.LANGUAGE_CODES_PUBLIC
        if lang not in available_langs:
            return error_response(
                'Язык "%s" не зарегистрирован в системе' % lang
            )

        translation.activate(lang)
        request.LANGUAGE_CODE = lang
        return None
