# Python3 code to demonstrate
# occurrence frequency using
# lambda + sum() + map()
from typing import Dict


def check_is_num(text: str) -> bool:
    for char in text:
        if char not in "0123456789.":
            return False
    return True





