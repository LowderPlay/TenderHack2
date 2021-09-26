import datetime
from csv_actions import *
from RA.DataSet.DataSet import *
from RA.Manager.Manager import *


space_name = "Original"
contracts = "Contracts"
CTE = "CTE"
manager = Manager(path=os.getcwd(), project_name=space_name)

# # Добавляем датасет "Контракты.xlsx"
# manager.add_DataSet(dataset=DataSet(dataset_name=contracts, show=True))
# manager.DataSet(contracts).load_csv_dataset(csv_file="Original/Contracts/Contracts_clean.csv", delimiter="$")
# # print(manager.DataSet(contracts))

# # Добавляем датасет "СТЕ.xlsx"
# manager.add_DataSet(dataset=DataSet(dataset_name=CTE, show=True))
# manager.DataSet(CTE).load_csv_dataset(csv_file="Original/CTE/CTE_clean.csv", delimiter="$")
# # print(manager.DataSet(CTE))

# # Собираем файл "KPGZ" (коды КПГЗ для OneHotEncoding)
# KPGZ = list(set(manager.DataSet(CTE).get_column(column="Код КПГЗ")))
# KPGZ.sort()
# manager.add_DataSet(dataset=DataSet(dataset_name="KPGZ"))
# manager.DataSet("KPGZ").create_empty_dataset()
# manager.DataSet("KPGZ").add_column(column="code", values=KPGZ)
# manager.DataSet("KPGZ").to_csv(path="Datasets/KPGZ.csv")

# # Собираем файл "IDtoKPGZ" (ID товара -> КПГЗ) для обобщения
# manager.add_DataSet(dataset=DataSet(dataset_name="IDtoKPGZ"))
# manager.DataSet("IDtoKPGZ").create_empty_dataset()
# manager.DataSet("IDtoKPGZ").add_column(column="ID СТЕ", values=manager.DataSet(CTE).get_column(column="ID СТЕ"))
# manager.DataSet("IDtoKPGZ").add_column(column="Код КПГЗ", values=manager.DataSet(CTE).get_column(column="Код КПГЗ"))
# manager.DataSet("IDtoKPGZ").to_csv(path="Datasets/IDtoKPGZ.csv")

id_to_kpgz = {}
kpgz_to_id = {}
manager.add_DataSet(dataset=DataSet(dataset_name="IDtoKPGZ", show=True))
manager.DataSet("IDtoKPGZ").load_csv_dataset(csv_file="Datasets/IDtoKPGZ.csv", delimiter=",")
for i in range(len(manager.DataSet("IDtoKPGZ"))):
    this_row = manager.DataSet("IDtoKPGZ").get_row(index=i)
    if this_row["ID СТЕ"] not in id_to_kpgz:
        id_to_kpgz[this_row["ID СТЕ"]] = this_row["Код КПГЗ"]
    if this_row["Код КПГЗ"] not in kpgz_to_id:
        kpgz_to_id[this_row["Код КПГЗ"]] = this_row["ID СТЕ"]
manager.delate_DataSet("IDtoKPGZ")

# # Собираем файл "Communications" (ID товара -> ID товара с которым он покупается)
# manager.add_DataSet(dataset=DataSet(dataset_name="Communications"))
# manager.DataSet("Communications").create_empty_dataset(columns_names=["ID", "with_ID"])
# for i in tqdm(range(len(manager.DataSet(contracts))), desc="Communications..."):
#     this_row = manager.DataSet(contracts).get_row(index=i)
#     comm = json.loads(str(this_row["СТЕ"]))
#     for outeri in range(len(comm)):
#         for inneri in range(outeri, len(comm[outeri:])):
#             # print(outeri, inneri, comm[outeri], comm[inneri])
#             if "fly" not in manager.datasets:
#                 manager.add_DataSet(dataset=DataSet(dataset_name="fly"))
#                 manager.DataSet("fly").create_empty_dataset(columns_names=manager.DataSet("Communications").get_keys())
#             if len(manager.DataSet("fly")) < 3500:
#                 if str(comm[outeri]['Id']) != str(comm[inneri]['Id']):
#                     manager.DataSet("fly").add_row(new_row={"ID": str(comm[outeri]['Id']),
#                                                             "with_ID": str(comm[inneri]['Id'])})
#             else:
#                 manager.DataSet("Communications").concat_DataSet(dataset=manager.DataSet("fly"))
#                 manager.delate_DataSet("fly")
# manager.DataSet("Communications").to_csv(path="Datasets/Communications.csv")

# # # Собираем файл "Graph_weights", подменяем ID'шники на КПГЗ и считаем кол-во повторяющихся, далее сохраняем
# manager.add_DataSet(dataset=DataSet(dataset_name="Communications"))
# manager.DataSet("Communications").load_csv_dataset(csv_file="Datasets/Communications.csv",
#                                                    delimiter=",")
# links = {}  # сперва записываем все связи
# data = []  # Нужна для быстрого создания датасета
# for i in tqdm(range(len(manager.DataSet("Communications"))), desc="Build Communications..."):
#     this_row = manager.DataSet("Communications").get_row(index=i)
#     try:
#         ID_KPGZ = id_to_kpgz[this_row["ID"]]
#         with_ID_KPGZ = id_to_kpgz[this_row["with_ID"]]
#         link = f"{ID_KPGZ}-{with_ID_KPGZ}"
#         if link not in links:
#             links[link] = 1
#         else:
#             links[link] += 1
#     except:
#         pass
# for link in tqdm(links, desc="Zip Communications..."):
#     data.append([str(link.split("-")[0]), str(link.split("-")[1]), str(links[link])])
# pd.DataFrame(data, columns=["KPGZ", "with_KPGZ", "count"]).to_csv("Datasets/Graph_weights.csv", index=False)

# Собираем файлик с дельтами дат по КРГЗ(чтобы знать, за сколько времени его можно начинать рекомендовать
manager.add_DataSet(dataset=DataSet(dataset_name=contracts, show=True))
manager.DataSet(contracts).load_csv_dataset(csv_file="Original/Contracts/Contracts_clean.csv", delimiter="$")
KPGZ_time_delta_dict = {}
data = []
for i in tqdm(range(len(manager.DataSet(contracts)))):
    this_row = manager.DataSet(contracts).get_row(index=i)
    try:
        public_date = this_row["Дата публикации КС на ПП"]
        contract_date = this_row["Дата заключения контракта"]
        order_time = datetime.datetime.strptime(public_date, "%Y-%m-%d %H:%M:%S.%f")
        done_time = datetime.datetime.strptime(contract_date, "%Y-%m-%d %H:%M:%S.%f")
        time_delta = (done_time - order_time).days
        if time_delta >= 0:
            CTE = json.loads(this_row["СТЕ"])
            for cte in range(len(CTE)):
                try:
                    KPGZ = id_to_kpgz[CTE[cte]['Id']]
                    if KPGZ not in KPGZ_time_delta_dict:
                        KPGZ_time_delta_dict[KPGZ] = [time_delta]
                    else:
                        KPGZ_time_delta_dict[KPGZ] += [time_delta]
                except:
                    pass
    except:
        pass
for KPGZ in tqdm(KPGZ_time_delta_dict, desc="KPGZ_Frequency..."):
    data.append([KPGZ, int(sum(KPGZ_time_delta_dict[KPGZ]) / len(KPGZ_time_delta_dict[KPGZ]))])
pd.DataFrame(data, columns=["KPGZ", "Frequency"]).to_csv("Datasets/KPGZ_Frequency.csv", index=False)