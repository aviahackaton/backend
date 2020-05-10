import time
import json
import psycopg2
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/upload'
cors = CORS(app)
app.config['JSON_AS_ASCII'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
app.url_map.strict_slashes = False

@cross_origin
@app.route('/api/v1/initialize/', methods=['GET'])
def initialize():
    if 'reports_num' not in reports_db:
        with reports_db.transaction():
            reports_db['reports_num'] = 0
    polys = [
        {
            "id": 0,
            "name": "United States",
            "coordinates": [
            {
                "lat": 55.80166847150037,
                "lon": 37.75216549902341
            },
            {
                "lat": 55.80862947567413,
                "lon": 37.87713498144529
            },
            {
                "lat": 55.731989658541536,
                "lon": 37.92382687597654
            },
            {
                "lat": 55.70951094778051,
                "lon": 37.74529904394527
            }
            ],
            "type": "red"
        },
        {
            "id": 1,
            "name": "Green",
            "coordinates": [
            {
                "lat": 55.77613409402249,
                "lon": 37.34979123144528
            },
            {
                "lat": 55.7784560956789,
                "lon": 37.411589327148405
            },
            {
                "lat": 55.725789932653754,
                "lon": 37.441801729492155
            },
            {
                "lat": 55.6955521084172,
                "lon": 37.35391110449215
            },
            {
                "lat": 55.75213194030574,
                "lon": 37.23718136816404
            }
            ],
            "type": "green"
        },
    ]
    report1 = {
        "coords": [55.80862947567413, 37.87713498144529],
        "square": 4,
        "areaPurpose": "Тип использования",
        "type": "Тип участка",
        "district": "Кадастровый номер квартала",
        "id": 0,
        "number": "Кадастровый номер1",
        "date": int(time.time()),
        "name": "United States",
    }

    report2 = {
        "coords": [55.75213194030574, 37.23718136816404],
        "square": 12,
        "areaPurpose": "Тип использования",
        "type": "Тип участка",
        "district": "Кадастровый номер квартала",
        "id": 1,
        "number": "Кадастровый номер2",
        "date": int(time.time()),
        "name": "Green",
    }
    with reports_db.transaction():
        reports_db[0] = json.dumps(report1)
        reports_db[1] = json.dumps(report2)
        reports_db.incr_by('reports_num', 2)
    with polygons_db.transaction():
        polygons_db[0] = json.dumps(polys[0])
        polygons_db[1] = json.dumps(polys[1])
    return 'Success', 200

@cross_origin
@app.route('/api/v1/poly/', methods=['GET'])
def polygons():
    res = []
    for i in range(int(reports_db['reports_num'])):
        polygon = json.loads(polygons_db[i])
        res.append(polygon)
    return jsonify(res)


@cross_origin
@app.route('/api/v1/upload/', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # work on the ... file
        #reports_db.incr('reports_num')
        #reports_db.commit()
    return 'Success', 200

@cross_origin
@app.route('/api/v1/reports/')
def get_reports():
    res = []
    for i in range(int(reports_db['reports_num'])):
        report = json.loads(reports_db[i])
        res.append({
            'id' : report['id'],
            'date' : report['date'],
            'name' : report['name'],
        })
    return jsonify(res)

@cross_origin
@app.route('/api/v1/reports/<id>/')
def get_report(id):
    try:
        report = json.loads(reports_db[id])
    except KeyError:
        return jsonify(None)
    polygon = json.loads(polygons_db[id])
    if report is not None:
        report['area'] = polygon
    return jsonify(report)


@cross_origin
@app.route('/api/v1/result/')
def mockup_result():
    polys = []
    with open('result.json', 'rb') as f:
        res = json.load(f)
    for key, value in res.items():
        poly = {
            "id": 1,
            "name": "Green",
            "type": "red",
            'coordinates' : [
                {
                    'lat' : coord[0],
                    'lng' : coord[1],
                }
                for coord in value
            ]
        }
        polys.append(poly)
    return jsonify(polys)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
