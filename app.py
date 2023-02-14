# -*- coding: utf-8 -*-
import json

from flask import Flask, jsonify, request, abort
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
import tldextract


app = Flask(__name__)


@app.route('/api/v1/domains', methods=['GET'])
def get_domains():
    site = request.args.get('site', None)
    if site is None:
        abort(400)

    return jsonify(json.dumps(list(get_resources(site))))


def get_resources(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        return set(map(lambda x: get_main_domains(x), driver.requests))
    finally:
        driver.quit()


def get_main_domains(req):
    extracted = tldextract.extract(urlparse(req.url).netloc)
    result = ".".join([extracted.domain, extracted.suffix])
    if extracted.subdomain:
        result = ".".join(['*', result])
    return result


if __name__ == '__main__':
    app.run(port=8000)
