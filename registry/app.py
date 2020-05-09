from flask import Flask
from selenium import webdriver
import time

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
#options.add_argument('--headless')
#options.add_argument('--no-sandbox')
#options.add_argument('--disable-dev-shm-usage')
options.binary_location = "/usr/bin/chromedriver"
driver = webdriver.Chrome(options=options)
driver.get('https://python.org')

"""
app = Flask(__name__)

@app.route('/registry/v1/buildings', methods=['GET'])
def polygons():
    return "hello"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
"""