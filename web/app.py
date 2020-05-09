from flask import Flask, jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app = Flask(__name__)
cors = CORS(app)
app.config['JSON_AS_ASCII'] = False
app.config['CORS_HEADERS'] = 'Content-Type'


@cross_origin
@app.route('/api/v1/poly', methods=['GET'])
def polygons():
    res = [
        {
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

    return jsonify(res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
