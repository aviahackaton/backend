import time
from flask import Flask, jsonify, request
from selenium import webdriver
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)
#

def get_registry_info(lat, lng, zoom=10):
    if lat is None or lng is None:
        return None 
    url = f"https://pkk.rosreestr.ru/#/search/{lat},{lng}/{zoom}/@qih8n8v9?text={lat}%20{lng}&type=1&inPoint=true&opened=77%3A1%3A1001%3A1484"
    driver.get(url)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup)
    info_body = soup.find('div', {'class' : 'detail-info-body'})
    if info_body is None:
        return None
    info_container = info_body.find('div', {'class' : 'vue-scrollbar__area'})
    items = info_container.find_all('div', {'class' : 'detail-info-item'})
    result = {
        item.find('div', {'class' : 'field-name'}).text.rstrip(':') :
        item.find('div', {'class' : 'expanding-box_content'}).text
        for item in items
    }
    return result

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/registry/v1/buildings', methods=['GET'])
def buildings():
    lat = request.args.get('lat', None)
    lng = request.args.get('lng', None)
    return jsonify(get_registry_info(lat, lng))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
