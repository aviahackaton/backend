import time
import json
import psycopg2
import os
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

DATABASE_HOST=os.environ.get('DB_HOST')
DATABASE_NAME=os.environ.get('DB_DATABASE')
DATABASE_USER=os.environ.get('DB_USER')
DATABASE_PASSWORD=os.environ.get('DB_PASSWORD')

conn = psycopg2.connect(dbname=DATABASE_NAME,
                        user=DATABASE_USER,
                        password=DATABASE_PASSWORD,
                        host=DATABASE_HOST,
                        port=5432)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS reports (id serial PRIMARY KEY, data TEXT);')
cursor.execute('CREATE TABLE IF NOT EXISTS polygons (id serial PRIMARY KEY, data TEXT);')
conn.commit()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/upload'
cors = CORS(app)
app.config['JSON_AS_ASCII'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
app.url_map.strict_slashes = False


@cross_origin
@app.route('/api/v1/initialize/', methods=['GET'])
def initialize():
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
        "coords": [55.75213194030574, 37.23718136816404],
        "square": "6 748 кв. м",
        "areaPurpose": "Для дачного строительства",
        "type": "Объект недвижимости",
        "district": "50:07:0090210",
        "id": 2,
        "number": "50:07:0090210:476",
        "date": int(time.time()),
        "name": "Московская область, Волоколамский район, с/п Осташевское, район д. Титово",
    }
    
    report2 = {
        "coords": [55.833964615925815, 35.807070509927144],
        "square": "69 988 кв. м",
        "areaPurpose": "Для общего пользования (уличная сеть)",
        "type": "Объект недвижимости",
        "district": "77:01:0001001",
        "id": 1,
        "number": "77:01:0001001:1484",
        "date": int(time.time()),
        "name": "г. Москва, Кремль, Большой сквер, Тайницкий сад",
    }

    cursor.execute('INSERT INTO reports (id, data) VALUES (%s, %s)', [report1['id'], json.dumps(report1),])
    cursor.execute('INSERT INTO reports (id, data) VALUES (%s, %s)', [report2['id'], json.dumps(report2),])
    cursor.execute('INSERT INTO polygons (id, data) VALUES (%s, %s)', [polys[0]['id'], json.dumps(polys[0]),])
    cursor.execute('INSERT INTO polygons (id, data) VALUES (%s, %s)', [polys[1]['id'], json.dumps(polys[1]),])
    conn.commit()
    return 'Success', 200

@cross_origin
@app.route('/api/v1/poly/', methods=['GET'])
def polygons():
    res = []
    cursor.execute('SELECT * FROM polygons ORDER BY id')
    polygons = cursor.fetchall()
    for row in polygons:
        polygon = json.loads(row[1])
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
    return 'Success', 200

@cross_origin
@app.route('/api/v1/reports/')
def get_reports():
    res = []
    cursor.execute('SELECT * FROM reports ORDER BY id')
    reports = cursor.fetchall()
    for row in reports:
        report = json.loads(row[1])
        res.append({
            'id' : report['id'],
            'date' : report['date'],
            'name' : report['name'],
        })
    return jsonify(res)

@cross_origin
@app.route('/api/v1/reports/<id>/')
def get_report(id):
    id = int(id)
    cursor.execute(f'SELECT * FROM reports WHERE id={id}')
    row = cursor.fetchone()
    if row is None:
        return jsonify(None)
    cursor.execute(f'SELECT * FROM polygons WHERE id={id}')
    poly = cursor.fetchone()
    report = json.loads(row[1])
    if poly is not None:
        polygon = json.loads(poly[1])
    else: polygon = None
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
            "name": key,
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
