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
                {
            "name": "poly2",
            "coordinates": [
            {
                "lat": 55.849678,
                "lon": 37.510379
            },
            {
                "lat": 55.836667,
                "lon": 37.675627
            },
            {
                "lat": 55.703241,
                "lon": 37.639402
            }
            ],
            "type": "red"
        },
                {
            "name": "Green",
            "coordinates": [
            {
                "lat": 55.819678,
                "lon": 37.510379
            },
            {
                "lat": 55.826667,
                "lon": 37.625627
            },
            {
                "lat": 55.733241,
                "lon": 37.639402
            },
                        {
                "lat": 55.693241,
                "lon": 37.669402
            },
                        {
                "lat": 55.703241,
                "lon": 37.659402
            }
            ],
            "type": "green"
        },
    ]

    return jsonify(res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
