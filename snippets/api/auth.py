from my.api.serializers import AccountShortSerializer


def jwt_response_payload_handler(token, user, request):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }

    """
    result = AccountShortSerializer(user, context={'request': request}).data
    result['token'] = token
    return result
