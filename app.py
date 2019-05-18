from flask import Flask, request, abort, jsonify, send_from_directory
from data_process import data_process
from get_functions import history_point_data
from radix_sort import radix_sort

import os

app = Flask(__name__)
path = 'bst_all.txt'
url = "https://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/Besttracks/bst_all.zip"
U = {'points':{'point1':{'longitude': 130.3, 'latitude':21.3, 'radius': 50000}, 'point2':{'longitude': 127.9, 'latitude':21.8, 'radius': 50000}, 'point3':{'longitude': 126.0, 'latitude':22.4, 'radius': 100000}, 'point4':{'longitude': 123.2, 'latitude':23.5, 'radius': 150000}, 'point5':{'longitude': 110.2, 'latitude':23.5, 'radius': 150000}, 'point6':{'longitude': 100.2, 'latitude':23.5, 'radius': 150000}}, 'parameter':{'w':'', 'n':10, 'month':0}}
user = {}

@app.route("/user_inputs", methods=['GET', 'POST'])
def user_inputs():
    if request.method == 'POST':
        global user
        user = request.get_json()
        print("This is POST request by WAYNA!")
        return user
    else:
        if user != {}:
            print("This is GET request by GANGAN's huspand!")
            return user
        else:
            print("This is GET request, but no input!")
            return 'user no input!'

@app.route("/typhoon_history")
def typhoon_history():
    return jsonify(data_process(url))

@app.route("/route_sorting")
def route_sorting():
    history = data_process(url) # everything
    point_data = history_point_data(history) # P(i, j)
    return jsonify(radix_sort(history, point_data, U))

@app.route('/report/<path:name>')
# 檔案在不在,在哪裡/有沒有亂戳,怎麼丟
def reportroute(name):
    name = 'index.html' if name is "" else name
    path = os.path.join("front", name)
    with open(path) as f:
        content = f.read()
    return content
