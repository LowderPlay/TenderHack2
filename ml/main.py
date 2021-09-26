import os
from graph import *
from tqdm import tqdm
from RA.DataSet.DataSet import *
from RA.Manager.Manager import *

manager = Manager(path=os.getcwd(), project_name="solution")

# # делаем предподготовку к запуску системы
# # 1) Создаём конвертеры ID -> КПГЗ и КПГЗ -> ID
# id_to_kpgz = {}
# kpgz_to_id = {}
# manager.add_DataSet(dataset=DataSet(dataset_name="IDtoKPGZ", show=True))
# manager.DataSet("IDtoKPGZ").load_csv_dataset(csv_file="Datasets/IDtoKPGZ.csv", delimiter=",")
# for i in tqdm(range(len(manager.DataSet("IDtoKPGZ"))), desc="Initialization ID -> KPGZ and KPGZ -> ID convertors..."):
#     this_row = manager.DataSet("IDtoKPGZ").get_row(index=i)
#     if this_row["ID СТЕ"] not in id_to_kpgz:
#         id_to_kpgz[this_row["ID СТЕ"]] = this_row["Код КПГЗ"]
#     if this_row["Код КПГЗ"] not in kpgz_to_id:
#         kpgz_to_id[this_row["Код КПГЗ"]] = this_row["ID СТЕ"]
# manager.delate_DataSet("IDtoKPGZ")


# # 2) Запускаем граф
# G = Graph()
# manager.add_DataSet(dataset=DataSet(dataset_name="Graph_weights", show=True))
# manager.DataSet("Graph_weights").load_csv_dataset(csv_file="Datasets/Graph_weights.csv", delimiter=",")
# for i in tqdm(range(len(manager.DataSet("Graph_weights"))), desc="Initialization graph weights..."):
#     this_row = manager.DataSet("Graph_weights").get_row(index=i)
#     G.add_edge(start_node_id=str(this_row["KPGZ"]),
#                end_node_id=str(this_row["with_KPGZ"]),
#                weight=int(this_row["count"]))
# manager.delate_DataSet("Graph_weights")
# traversal = G.graph_traversal(start_id="01.13.17.17", abs_level=6, min_similarity=55, max_similarity=65)
# for t in traversal:
#     print(t, traversal[t])

