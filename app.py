### Environment
from flask import Flask, request, abort, jsonify, send_from_directory, json
import os
import threading as td

### /route_sorting (Manual + Center)
from data_process import data_process
from get_functions import history_point_data
from radix_sort import radix_sort

### /typhoon_forecast (Center)
from center.api import get_typhoon_track, get_typhoons, get_alive_typhoons
from center.search import list_similar_typhoons, forecast_points, get_latest_link

app = Flask(__name__)
url = "https://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/Besttracks/bst_all.zip"

@app.route("/route_sorting", methods = ["GET"])
### Get the toPOST(dict: points, parameters) and return the outcome(dict: order) ###
def route_sorting():

    try:
        toPOST = request.args.get('toPOST') # user input points
    except:
        print("GET failed")
        return jsonify({"message":"request body is not json."}), 400

    if toPOST != {}:
        print("RADIX SORT START!")

        ### Process history data
        try:
            history = data_process(url) # entire historical typhoon tracks
            point_data = history_point_data(history) # P(i, j)
        except:
            return jsonify({"message":"Defective JMA API."}), 406

        ### Process similarity model
        try:
            U = json.loads(toPOST) # convert user inputs to dict
        except:
            return jsonify({"message":"Wrong fromat in points data."}), 400

        ### Success
        return jsonify(radix_sort(history, point_data, U))
    else:
        print('NO USER INPUTS!')
        return jsonify({"message":"user input is empty."}), 400

@app.route("/typhoon_forecast", methods = ["GET"])
### Crawl the typhoon2000(default: CWB) and return toPOST(dict: points, parameters) ###
def typhoon_forecast():

    try:
        member = ['HKO', 'JTWC', 'JMA', 'NMC', 'CWB', 'KMA']
        ret = {}

        for i in range(len(get_alive_typhoons())):

            # Record the info of the latest typhoon
            en, zh, year, key = get_typhoons()[i]
            code, link = get_latest_link(i + 1)

            ret[en] = {}
            ret[en]['info'] = {"en": en, "zh": zh, "year": year, "code": code, "links": link}

            word = '%s (%s)' % (zh, en) if zh != '' else en
            print('%d最新的颱風是：%s，代碼：%s' % (year, word, code))

            # Record the forecast points of each center
            for center in member:
                track = get_alive_typhoons(member = center)[key]
                ret[en][center] = forecast_points(track)

        return jsonify(ret)

    except: # If typhoon2000 is not available
        return jsonify({"message":"Forecast center's database(typhoon2000) is not available"}), 423

@app.route("/typhoon_history")
### Crawl the JMA and return entire historical typhoon points data ###
def typhoon_history():
    return jsonify(data_process(url))

@app.route('/')
def index():
    return send_from_directory('front', 'index.html')

@app.route('/<path:name>')
# 檔案在不在,在哪裡/有沒有亂戳,怎麼丟
def reportroute(name):
    name = 'index.html' if name is "" else name
    return send_from_directory('front', name)
