
import datetime
from RA.DataSet.DataSet import *
from RA.Manager.Manager import *


space_name = "Original"
contracts = "Contracts"
CTE = "CTE"


manager = Manager(path=os.getcwd(), project_name=space_name)

# Добавляем датасет "Контракты.xlsx"
manager.add_DataSet(dataset=DataSet(dataset_name=contracts, show=True))
manager.DataSet(contracts).load_csv_dataset(csv_file="Original/Contracts/Contracts_clean.csv", delimiter="$")
# print(manager.DataSet(contracts))

# Добавляем датасет "СТЕ.xlsx"
# manager.add_DataSet(dataset=DataSet(dataset_name=CTE, show=True))
# manager.DataSet(CTE).load_csv_dataset(csv_file="Original/CTE/CTE_clean.csv", delimiter="$")
# print(manager.DataSet(CTE))

"Дата публикации КС на ПП"
"Дата заключения контракта"
# order_time = datetime.datetime.strptime("2019-06-13 17:07:08.753",
#                                         "%Y-%m-%d %H:%M:%S.%f")
# done_time = datetime.datetime.strptime("2019-06-13 18:07:08.753",
#                                        "%Y-%m-%d %H:%M:%S.%f")
# print((done_time - order_time).days)

