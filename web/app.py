from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/api/v1/poly', methods=['GET'])
def polygons():

    res = [
          {
            "name": "United States",
            "coordinates": [
            {
                "lat": 55.869678,
                "lon": 37.530379
            },
            {
                "lat": 55.856667,
                "lon": 37.695627
            },
            {
                "lat": 55.723241,
                "lon": 37.609402
            }
            ],
            "type": "red"
        },
    ]

    return jsonify(res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
