import datetime


def save_leading_zero(v):
    """Excel при открытии csv файла съедает лидирующие нули
    Чтобы этого избежать мы оборачиваем значение в формулу,
    но не делаем этого если строка содержит дату
    или уже является гиперссылкой
    """
    if isinstance(v, str):
        if v.startswith('='):
            return v
        try:
            datetime.datetime.strptime(v, '%d.%m.%Y')
        except ValueError:
            return '="%s"' % v
    return v
