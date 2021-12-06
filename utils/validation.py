from decimal import Decimal


def is_float(value: str) -> bool:
    return value.replace('.', '', 1).isdigit()


def is_valid_enum_list(enums: list[str]):
    if not len(enums) or len(enums) % 2:
        return False
    total_sum = Decimal(0.0)
    for enum_pair in zip(*[iter(enums)] * 2):
        if not is_float(enum_pair[1]) or float(enum_pair[1]) < 0.0:
            return False
        total_sum += Decimal(float(enum_pair[1]))
    if total_sum < 99.0 or total_sum > 101.0:
        return False
    return True


def is_valid_name(name: str) -> bool:
    return not name[0].isdigit() and not '.' in name and not ' ' in name and len(name)
