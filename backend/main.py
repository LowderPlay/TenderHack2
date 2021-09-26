#!flask/bin/python
import time
from graph import *
from converter import *
from random import random
from flask import Flask, jsonify
from mysql.connector import connect
from datetime import *


def season_loader(season_data: pd.DataFrame):
    KPGZ_season = {}
    for i in range(len(season_data)):
        KPGZ_season[season_data.at[i, "Date"]] = str(season_data.at[i, "Season"]).split(":")
    return KPGZ_season


G = Graph()
connection = connect(host="localhost",
                     port='3306',
                     user="root",
                     password="root",
                     database="dataset")
cursor = connection.cursor()
KPGZ_ID = id_to_kpgz(pd.read_csv('dataset/IDtoKPGZ.csv'))
KPGZ_code = list(pd.read_csv('dataset/KPGZ_code.csv')['code'].to_list())
KPGZ_season = season_loader(season_data=pd.read_csv("dataset/KPGZ_Season.csv", sep=","))
graph_weights = pd.read_csv('dataset/Graph_weights.csv', delimiter=",")
launch_graph(graph_weights, G)
app = Flask(__name__)


def season_worker(date, KPGZ_season):
    KPGZs = []
    date = datetime.strptime(date, '%m-%d')
    for s in KPGZ_season:
        if abs((date - datetime.strptime(s, '%m-%d')).days) < 1:
            KPGZs += KPGZ_season[s]
    return list(set(KPGZs))


def graph(product_list):
    recommend_product = []
    for elem in product_list:
        try:
            traversal = G.graph_traversal(start_id=elem, abs_level=3, min_similarity=55, max_similarity=65)
            recommend_product.extend(traversal[2])
        except:
            pass
    return list(set(recommend_product))


@app.route('/api/provider/<string:date>', methods=['GET'])
def get_provider_itm(date):

    return jsonify({'products': season_worker(date, KPGZ_season)})


@app.route('/api/customer/<int:itm>&<string:date>', methods=['GET'])
def get_customer_itm(itm, date):
    cursor.execute(
        f"""SELECT * FROM json_table((SELECT json_extract(json_arrayagg(`СТЕ`), 
            '$**.Id') as ids FROM dataset.contracts
            WHERE `ИНН заказчика` = {itm}), '$[*]'
            columns(id int path '$')) as jt;""")
    data_product = graph(product_to_encode(cursor.fetchall(), KPGZ_ID))
    ml_data = season_worker(date, KPGZ_season)
    print(data_product)
    print(ml_data)
    return jsonify({'products': list(set(data_product) & set(ml_data))})


app.run(debug=True)
