import os
import re
import json
import math
import pandas as pd
from tqdm import tqdm
from methods import *
from graph import *
from contrackts_row import *
from RA.DataSet.DataSet import *


#  Читаем первоначальный, огромный файлик
original_dataset = DataSet(dataset_project_name="original_dataset", show=True)
original_dataset.load_csv_dataset(csv_file="TenderHackDataset/Example_Tender_Hack.csv",
                                  delimiter=";")
# original_dataset.load_csv_dataset(csv_file="TenderHackDataset/DataSet_EKB_200000.csv", delimiter="~") # новый
# original_dataset.load_DataFrame(dataframe=pd.read_excel('TenderHackDataset/DataSet_EKB_200000.xlsx',
#                                                         sheet_name='200000ste'))
# original_dataset.fillna()
# original_dataset.export(dataset_name="DataSet_EKB_200000",
#                         dataset_folder="TenderHackDataset/",
#                         including_json=False,
#                         including_plots=False,
#                         encoding='utf-8',
#                         delimeter="~")

print(original_dataset)
# column = original_dataset.get_column_info(column_name="Другая продукция в контрактах", extended=True)
# str_stat = column
# print(str_stat.get_str_stat().get_letter_counter())
# quit()

# # Получение значения с колонки
# ids = DataSet(dataset_project_name="some", show=True)
# ids.create_empty_dataset()
# ids.delete_column(column="Просмотры")
# ids.add_column(column="Просмотры",
#                values=original_dataset.get_column(column="Просмотры"),
#                dif_len=True)
# ids.export(dataset_name="Просмотры",
#            dataset_folder="some",
#            including_plots=False,
#            including_json=False)
# some = [float(i) for i in original_dataset.get_column(column="Просмотры") if not math.isnan(i)]
# some.sort()
# print("ids", min(some), max(some), set(some))
# quit()

# Разрезаем его на файлики поменьше по 1000 записей
# tender_dataset = None
# for i in tqdm(range(len(original_dataset)), desc="Splitting (1000)..."):
#     if tender_dataset is None:
#         tender_dataset = DataSet(dataset_project_name="TenderDataSet", show=True)
#         tender_dataset.create_empty_dataset(columns_names=original_dataset.get_keys())
#     tender_dataset.add_row(new_row=original_dataset.get_row(index=i))
#     if i % 1000 == 0 and i != 0:
#         tender_dataset.export(dataset_name=f"TenderDataSet_X{i}",
#                               dataset_folder="Splitted_X1000_TenderHack",
#                               including_json=False,
#                               including_plots=False,
#                               encoding='utf-8',
#                               delimeter="~")
#         tender_dataset = DataSet(dataset_project_name="TenderDataSet", show=True)
#         tender_dataset.create_empty_dataset(columns_names=original_dataset.get_keys())
# tender_dataset.export(dataset_name=f"TenderDataSet_X200000",
#                       dataset_folder="Splitted_X1000_TenderHack",
#                       including_json=False,
#                       including_plots=False,
#                       encoding='utf-8',
#                       delimeter="~")
# quit()

# Делаем преобразование файлов(чистка и всё такое)
G = Graph()  # класс графа
specifics = {}
folders = os.listdir("Splitted_X1000_TenderHack")
folders = sorted(folders, key=lambda x: int(str(x).split("_")[1].replace("X", "").replace("+", "")))
for file in tqdm(folders):
    fly_dataset = DataSet(dataset_project_name=f"fly_dataset X {file}", show=True)
    fly_dataset.load_csv_dataset(csv_file=os.path.join("Splitted_X1000_TenderHack", file, f"{file}.csv"),
                                 delimiter="~")
    fly_dataset.fillna()
    for fd in range(len(fly_dataset)):
        this_row = fly_dataset.get_row(index=fd)
        row = Row(this_row=this_row)
        # Нужно по характеристикам предсказывать!!!
        for rsS in row.specifications_STE:
            try:
                if rsS['Name'] not in specifics:
                    specifics[rsS['Name']] = 1
                else:
                    specifics[rsS['Name']] += 1
            except:
                print(rsS)
specifics = dict(sorted(specifics.items(), key=lambda x: x[1], reverse=True))
specifics_dataset = DataSet(dataset_project_name="specifics")
specifics_dataset.create_empty_dataset(columns_names=list(specifics.keys())[:500])
specifics_dataset.export(delimeter="~")
quit()
print(list(specifics.keys())[:500])
for sk in specific_keys:
    print(sk, specific_keys[sk])
# print(len(G))
# traversal = G.graph_traversal(start_id=str(28145480), abs_level=25)
# for t in traversal:
#     print(t, traversal[t])
# quit()
