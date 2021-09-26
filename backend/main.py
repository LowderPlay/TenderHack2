#!flask/bin/python
import time
from graph import *
from converter import *
from random import random
from flask import Flask, jsonify
from mysql.connector import connect


G = Graph()
connection = connect(host="localhost",
                     port='3306',
                     user="root",
                     password="root",
                     database="dataset")
cursor = connection.cursor()
KPGZ_ID = id_to_kpgz(pd.read_csv('dataset/IDtoKPGZ.csv'))
KPGZ_code = list(pd.read_csv('dataset/KPGZ_code.csv')['code'].to_list())
graph_weights = pd.read_csv('dataset/Graph_weights.csv', delimiter=",")
launch_graph(graph_weights, G)
app = Flask(__name__)

# Для тестов сезонности
def ML(date):
    f = []
    for i in range(5230):
        f.append(round(random()))
    return f


def graph(product_list):
    recommend_product = []
    for elem in product_list:
        try:
            traversal = G.graph_traversal(start_id=elem, abs_level=3, min_similarity=55, max_similarity=65)
            recommend_product.extend(traversal[2])
        except:
            print(elem)
            pass
    return list(set(recommend_product))

@app.route('/api/provider/<string:date>', methods=['GET'])
def get_provider_itm(date):
    data_ml = binary_to_encode(ML(date), KPGZ_code)

    return jsonify({'products': data_ml})


@app.route('/api/customer/<int:itm>&<string:date>', methods=['GET'])
def get_customer_itm(itm, date):
    cursor.execute(
        f"""SELECT * FROM json_table((SELECT json_extract(json_arrayagg(`СТЕ`), 
            '$**.Id') as ids FROM dataset.contracts
            WHERE `ИНН заказчика` = {itm}), '$[*]'
            columns(id int path '$')) as jt;""")
    data_ml = binary_to_encode(ML(date), KPGZ_code)
    data_product = graph(product_to_encode(cursor.fetchall(), KPGZ_ID))
    return jsonify({'products': list(set(data_product) & set(data_ml))})


app.run(debug=True)
