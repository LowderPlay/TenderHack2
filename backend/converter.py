import pandas as pd
from typing import Dict
from datetime import datetime, timedelta


def date_to_number(date_time: str):
    return datetime.strptime(date_time, '%Y-%m-%d').timetuple().tm_yday


def number_to_date(year_day: int):
    return datetime(datetime.today().timetuple().tm_year, 1, 1) + timedelta(year_day - 1)


def binary_to_encode(bin_elements: list, data):
    encode_elements = []
    for index in range(len(bin_elements)):
        if bin_elements[index] == 1:
            encode_elements.append(data[index])
    return encode_elements


def product_to_encode(product_elements, data):
    encode_elements = []
    for elem in product_elements:
        elem = int(elem[0])
        if elem in data:
            encode_elements.append(data[elem])
    return encode_elements


def id_to_kpgz(data: pd.DataFrame) -> Dict[str, str]:
    kpgz_elements = {}
    for i in range(len(data)):
        elem = data.at[i, 'ID СТЕ']
        if elem not in kpgz_elements:
            kpgz_elements[elem] = data.at[i, 'Код КПГЗ']
    return kpgz_elements

