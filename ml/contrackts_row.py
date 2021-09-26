import json
import math


class ContractsRow:
    def __init__(self, this_row: dict):
        self.contract_number = str(this_row["Номер контракта"])
        self.publication_date = str(this_row["Дата публикации КС на ПП"])
        self.conclusion_date = this_row["Дата заключения контракта"]
        self.contract_price = this_row["Цена контракта"]
        self.customers_IIN = str(this_row["ИНН заказчика"])
        self.customers_KPP = str(this_row["КПП заказчика"])
        self.customers_name = str(this_row["Наименование заказчика"])
        self.suppliers_IIN = str(this_row["ИНН заказчика"])
        self.suppliers_KPP = str(this_row["КПП заказчика"])
        self.suppliers_name = str(this_row["Наименование поставщика"])
        self.CTE = str(this_row["СТЕ"])


# def convert_date(date_time: str):
#     date = date_time.split("  ")[0]
#     print(date)
#     YYYY = date.split(".")[2]
#     MM = date.split(".")[1]
#     DD = date.split(".")[0]
#     time = date_time.split("  ")[1]
#     return f"{YYYY}-{MM}-{DD} {time}"


def convert_price(price: str):
    return float(price.replace(",", "."))


def transform_contracts(this_row):
    this_row["Номер контракта"] = str(this_row["Номер контракта"])
    this_row["Дата публикации КС на ПП"] = this_row["Дата публикации КС на ПП"]
    this_row["Дата заключения контракта"] = this_row["Дата заключения контракта"]
    this_row["Цена контракта"] = convert_price(str(this_row["Цена контракта"]))
    this_row["ИНН заказчика"] = str(this_row["ИНН заказчика"])
    this_row["КПП заказчика"] = str(this_row["КПП заказчика"])
    this_row["Наименование заказчика"] = str(this_row["Наименование заказчика"])
    this_row["ИНН заказчика"] = str(this_row["ИНН заказчика"])
    this_row["КПП заказчика"] = str(this_row["КПП заказчика"])
    this_row["Наименование поставщика"] = str(this_row["Наименование поставщика"])
    CTE = this_row["СТЕ"]
    try:
        if len(CTE) >= 32000:
            CTE = CTE[:CTE.rindex(',{')] + "]"
        CTE = json.loads(str(CTE))
        to_delate = [i for i in range(len(CTE)) if CTE[i]['Id'] is None]
        for i in to_delate[::-1]:
            del CTE[i]
        this_row["СТЕ"] = json.dumps(CTE)
    except Exception as e:
        print(CTE)

    if (this_row["СТЕ"] != "[]" and this_row["СТЕ"] != "-"):
        for tr in this_row:
            try:
                if math.isnan(this_row[tr]) or None:
                    return None
            except:
                pass
            try:
                if this_row[tr] == "nan":
                    return None
            except:
                pass
        return this_row
    else:
        return None
