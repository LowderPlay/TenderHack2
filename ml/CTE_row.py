import json
import math


class CTERow:
    def __init__(self, this_row: dict):
        self.contract_number = str(this_row["ID СТЕ"])
        self.publication_date = str(this_row["Название СТЕ"])
        self.conclusion_date = str(this_row["Категория"])
        self.contract_price = str(this_row["Код КПГЗ"])
        self.customers_IIN = str(this_row["Характеристики"])


def transform_CTE(this_row):
    this_row["ID СТЕ"] = str(this_row["ID СТЕ"])
    this_row["Название СТЕ"] = str(this_row["Название СТЕ"])
    this_row["Категория"] = str(this_row["Категория"])
    this_row["Код КПГЗ"] = str(this_row["Код КПГЗ"])
    this_row["Характеристики"] = str(this_row["Характеристики"])
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
    # try:
    #     if len(CTE) >= 32000:
    #         CTE = CTE[:CTE.rindex(',{')] + "]"
    #     CTE = json.loads(str(CTE))
    #     to_delate = [i for i in range(len(CTE)) if CTE[i]['Id'] is None]
    #     for i in to_delate[::-1]:
    #         del CTE[i]
    #     this_row["СТЕ"] = json.dumps(CTE)
    #     # print(this_row["СТЕ"])
    # except Exception as e:
    #     print(CTE)
    #
    # if (this_row["СТЕ"] != "[]" and this_row["СТЕ"] != "-"):
    #     for tr in this_row:
    #         try:
    #             if math.isnan(this_row[tr]) or None:
    #                 return None
    #         except:
    #             pass
    #         try:
    #             if this_row[tr] == "nan":
    #                 return None
    #         except:
    #             pass
    #     return this_row
    # else:
    #     return None
