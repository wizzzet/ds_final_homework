from collections import defaultdict


def nested_defaultdict():
    return defaultdict(nested_defaultdict)


def unique_list(seq):
    """
    Возвращает список уникальных элементов последовательности,
    сохраняя их порядок
    """
    no_duplicates = []
    return [no_duplicates.append(i) for i in seq if not no_duplicates.count(i)]
