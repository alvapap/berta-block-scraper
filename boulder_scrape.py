import requests
import re
from prometheus_client import Gauge, Counter, start_http_server
import time
import os
import logging

g = Gauge('free_spots', 'The number of free spots in Berta Block')
c = Counter('request_error', 'Count the exceptios triggered by requesting the url')
default_url = 'https://144.webclimber.de/de/trafficlight?callback=WebclimberTrafficlight.insertTrafficlight&key=ZF59sAT398kR3G5gCEF8tNuqqZf026zw&hid=144&container=trafficlightContainer&type=&area='
url = os.getenv('WEBCLIMBER_URL', default_url)

def getAvailabbleSpots():
    try:
        page = requests.get(url)
        pattern = '\((\d+)(?:\sfreie)'
        result = re.search(pattern, str(page.content))
        g.set(result.group(1))
    except requests.exceptions.RequestException as e:
        logging.error(e)
        c.inc()

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8080)
    # Generate some requests.
    while True:
        getAvailabbleSpots()
        time.sleep(60)