import os
import tqdm
import openpyxl
from RA.DataSet.DataSet import *
from RA.Manager.Manager import *

from contrackts_row import *
from CTE_row import *


space_name = "Original"
contracts = "Contracts"
contracts_clear = contracts + "_clear"
CTE = "CTE"
CTE_clear = CTE + "_clear"
manager = Manager(path=os.getcwd(), project_name=space_name)

# Добавляем датасет "Контракты.xlsx"
manager.add_DataSet(dataset=DataSet(dataset_name="Contracts", show=True))
manager.DataSet(contracts).load_xlsx_dataset(xlsx_file="TenderHackDataset/Контракты.xlsx", sheet_name="Запрос1")
print(manager.DataSet(contracts))

# Добавляем датасет "СТЕ.xlsx"
manager.add_DataSet(dataset=DataSet(dataset_name="CTE", show=True))
manager.DataSet(CTE).load_xlsx_dataset(xlsx_file="TenderHackDataset/СТЕ.xlsx", sheet_name="Запрос1")
print(manager.DataSet(CTE))

# Ищем частотность символов в датасете "Контракты.xlsx"
for key in manager.DataSet(contracts).get_keys():
    column = manager.DataSet(contracts).get_column_info(column_name=key, extended=False)
    if column.get_type().startswith("str"):
        column_EXTENDED = manager.DataSet(contracts).get_column_info(column_name=key, extended=True)
        print(column_EXTENDED.get_str_stat().get_letter_counter())

# Ищем частотность символов в датасете "СТЕ.xlsx"
for key in manager.DataSet(CTE).get_keys():
    column = manager.DataSet(CTE).get_column_info(column_name=key, extended=False)
    if column.get_type().startswith("str"):
        column_EXTENDED = manager.DataSet(CTE).get_column_info(column_name=key, extended=True)
        print(column_EXTENDED.get_str_stat().get_letter_counter())

# Заменяем "$" на " ", во всех колонках датасета "Контракты.xlsx", устанавливаем "$" как разделитель и сохраняем в .csv
for key in manager.DataSet(contracts).get_keys():
    print(contracts, key)
    column = manager.DataSet(contracts).get_column_info(column_name=key, extended=False)
    if column.get_type().startswith("str"):
        for i in tqdm(range(len(manager.DataSet(contracts))), desc=contracts + "_" + key):
            some_str_value = str(manager.DataSet(contracts).get_from_field(column=key, index=i))
            if "$" in some_str_value:
                manager.DataSet(contracts).set_to_field(column=key, index=i, value=some_str_value.replace("$", ""))
manager.DataSet(contracts).set_delimiter("$")
manager.DataSet(contracts).export()

# Заменяем "$" на " ", во всех колонках датасета "CTE.xlsx", устанавливаем "$" как разделитель и сохраняем в .csv
for key in manager.DataSet(CTE).get_keys():
    print(CTE, key)
    column = manager.DataSet(CTE).get_column_info(column_name=key, extended=False)
    if column.get_type().startswith("str"):
        for i in tqdm(range(len(manager.DataSet(CTE))), desc=contracts + "_" + key):
            some_str_value = str(manager.DataSet(CTE).get_from_field(column=key, index=i))
            if "$" in some_str_value:
                manager.DataSet(CTE).set_to_field(column=key, index=i, value=some_str_value.replace("$", ""))
manager.DataSet(CTE).set_delimiter("$")
manager.DataSet(CTE).export()

# # Открываем Contracts.csv, заполняем откровенные null, убираем null-овые значения из json
# manager.add_DataSet(dataset=DataSet(dataset_name=contracts, show=True))
# manager.DataSet(contracts).load_csv_dataset(csv_file="Original\Contracts\Contracts.csv", delimiter="$")
manager.DataSet(contracts).set_field_types(new_fields_type=str, exception={"Цена контракта": float})
manager.DataSet(contracts).fillna()
manager.add_DataSet(dataset=DataSet(dataset_name=contracts + "_clear"))
manager.DataSet(contracts_clear).create_empty_dataset(columns_names=manager.DataSet(contracts).get_keys())
for i in tqdm(range(len(manager.DataSet(contracts))), desc=contracts + " transforming..."):
    if "fly" not in manager.datasets:
        manager.add_DataSet(dataset=DataSet(dataset_name="fly"))
        manager.DataSet("fly").create_empty_dataset(columns_names=manager.DataSet(contracts).get_keys())
    if len(manager.DataSet("fly")) < 3500:
        row = transform_contracts(this_row=manager.DataSet(contracts).get_row(index=i))
        if row is not None:
            manager.DataSet("fly").add_row(new_row=row)
    else:
        manager.DataSet(contracts_clear).concat_DataSet(dataset=manager.DataSet("fly"))
        manager.delate_DataSet("fly")
manager.DataSet(contracts_clear).add_column(column="ID",
                                            values=[i for i in range(len(manager.DataSet(contracts_clear)))])
manager.DataSet(contracts_clear).delete_column(column="КПП заказчика")
manager.DataSet(contracts_clear).delete_column(column="КПП поставщика")
manager.DataSet(contracts_clear).to_csv(path="Original\Contracts\Contracts_clean.csv", delimeter="$")
manager.DataSet(contracts_clear).to_excel(path="TenderHackDataset\Контракты(очищенные).xlsx", sheet_name="Запрос1")
print(manager.DataSet(contracts_clear))
quit()

# # # Открываем CTE.csv, заполняем откровенные null, убираем null-овые значения из json
# manager.add_DataSet(dataset=DataSet(dataset_name=CTE, show=True))
# manager.DataSet(CTE).load_csv_dataset(csv_file="Original\CTE\CTE.csv", delimiter="$")
manager.DataSet(CTE).set_field_types(new_fields_type=str, exception={"Характеристики": str})
manager.DataSet(CTE).fillna()
manager.add_DataSet(dataset=DataSet(dataset_name=CTE_clear))
manager.DataSet(CTE_clear).create_empty_dataset(columns_names=manager.DataSet(CTE).get_keys())
for i in tqdm(range(len(manager.DataSet(CTE))), desc=CTE + " transforming..."):
    if "fly" not in manager.datasets:
        manager.add_DataSet(dataset=DataSet(dataset_name="fly"))
        manager.DataSet("fly").create_empty_dataset(columns_names=manager.DataSet(CTE).get_keys())
    if len(manager.DataSet("fly")) < 3500:
        row = transform_CTE(this_row=manager.DataSet(CTE).get_row(index=i))
        if row is not None:
            manager.DataSet("fly").add_row(new_row=row)
    else:
        manager.DataSet(CTE_clear).concat_DataSet(dataset=manager.DataSet("fly"))
        manager.delate_DataSet("fly")
manager.DataSet(CTE_clear).to_csv(path="Original\CTE\CTE_clean.csv", delimeter="$")
manager.DataSet(CTE_clear).to_excel(path="TenderHackDataset\CTE(очищенное).xlsx", sheet_name="Запрос1")
print(manager.DataSet(CTE_clear))


