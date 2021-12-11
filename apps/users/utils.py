import hashlib

from snippets.api.exceptions import APIProcessError


def get_user_auth_token_subject(user):
    salt_hash = hashlib.sha256(user.token_salt.encode('utf-8')).hexdigest()
    return ''.join([x for i, x in enumerate(salt_hash) if i % 4 == 0])


def get_user_restore_token_subject(user):
    if not user.restore_salt:
        raise APIProcessError(
            'Ошибка при попытке создать ссылку восстановления'
        )

    salt_hash = hashlib.sha256(user.restore_salt.encode('utf-8')).hexdigest()
    return ''.join([x for i, x in enumerate(salt_hash) if i % 4 == 0])
