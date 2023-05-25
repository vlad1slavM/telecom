import re


def validate_serial_number(mask: str, serial_number: str) -> bool:
    """
    Валидатор серийного номера
    :param mask: Маска оборудования
    :param serial_number: Серийный номер
    """
    pattern = ''
    regex_dict = {
        'N': '[0-9]',
        'A': '[A-Z]',
        'a': '[a-z]',
        'X': '[A-Z0-9]',
        'Z': '[-_@]',
    }
    for letter in mask:
        if letter in regex_dict:
            pattern += regex_dict[letter]
        else:
            return False

    return bool(re.match(pattern, serial_number))
