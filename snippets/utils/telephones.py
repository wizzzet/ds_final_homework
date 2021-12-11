import re


def prepare_telephone_number(phone_number):
    phone_number = re.sub(r'[^0-9]+', '', phone_number.lower().strip())
    # специально для России и Казахстана
    if phone_number.startswith('8'):
        phone_number = '7' + phone_number[1:]

    return phone_number
