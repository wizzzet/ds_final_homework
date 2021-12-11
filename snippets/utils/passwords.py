import random
import string

DEFAULT_ALT_ID_SAMPLE = string.ascii_lowercase + string.digits
DEFAULT_PASSWORD_SAMPLE = string.ascii_lowercase + string.digits
DEFAULT_RECOVERY_TOKEN_SAMPLE = string.ascii_lowercase + string.digits
DEFAULT_TOKEN_SAMPLE = string.ascii_letters + string.digits


def generate_random_string(length=16, sample=DEFAULT_TOKEN_SAMPLE):
    lst = [random.choice(sample) for _ in range(length)]
    return ''.join(lst)


def generate_alt_id(length=30, sample=DEFAULT_ALT_ID_SAMPLE):
    """Создание альтернативного ID"""
    return generate_random_string(length=length, sample=sample)


def generate_password(length=8, sample=DEFAULT_PASSWORD_SAMPLE):
    """Создание пароля пользователя"""
    return generate_random_string(length=length, sample=sample)


def generate_recovery_token(length=80, sample=DEFAULT_RECOVERY_TOKEN_SAMPLE):
    """Создание реферрального кода пользователя"""
    return generate_random_string(length=length, sample=sample)
