import json
from urllib import request

import time
from flask import Flask, jsonify, render_template

app = Flask(__name__)

SEED = "1576246343000"
LIVE_DATA_URL = "https://api.gambite.me/api/v1/live/brand/1773043987561717760/zh/" + SEED

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/live')
def live():
    response = request.urlopen(LIVE_DATA_URL)
    res_json = json.loads(response.read().decode('utf-8'))
    items = res_json['items']

    match_ids = []
    for item in items:
        if item[0][1] == 'desc':
            sport = item[1]['sport']['id']
            if sport == '1': # 足球
                dict_tmp = {}
                match = item[1]
                if match:
                    match_id = match['betradar_id'].replace("sr:match:","")
                    dict_tmp['id'] = match_id
                    if 'scheduled' in match:
                        begin_second = match['scheduled'] # 秒
                        current_second = int(time.time())
                        if (current_second - begin_second)/60 >=100:
                            continue
                    if 'betradar_h2h' in match:
                        url =  match['betradar_h2h']
                        dict_tmp['url'] = url
                    match_ids.append(dict_tmp)
    return render_template('show.html', ids=match_ids)

if __name__ == '__main__':
    app.run()

