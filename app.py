from flask import Flask, request, abort, jsonify, send_from_directory
from data_process import data_process
from get_functions import history_point_data
from radix_sort import radix_sort

app = Flask(__name__)
path = 'bst_all.txt'
url = "https://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/Besttracks/bst_all.zip"
U = {'point1':{'longitude': 123.0, 'latitude':24.5, 'radius': 1000000}, 'point2':{'longitude': 120.0, 'latitude':28.5, 'radius': 1000000}, 'point3':{'longitude': 110.0, 'latitude':30.5, 'radius': 500000}, 'point4':{'longitude': 100.0, 'latitude':40.5, 'radius': 1500000}, 'point5':{'longitude': 90.0, 'latitude':38.5, 'radius': 1500000}}

@app.route("/typhoon_history")
def typhoon_history():
    return jsonify(data_process(path))

@app.route("/route_sorting")
def route_sorting():
    return jsonify(radix_sort(path, U))
