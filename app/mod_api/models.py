"""
models.py

Api module models.
"""
import requests
from flask import current_app, abort


class MyAdventure(object):
    def __init__(self):
        pass

    @staticmethod
    def get(path):
        r = requests.get(current_app.config['API_URL'] + '/api/v1' + path)
        if r.status_code != 200:
            abort(r.status_code)
        return r.json()

    @staticmethod
    def post(path, data):
        r = requests.post(current_app.config['API_URL'] + '/api/v1' + path, data=data)
        if r.status_code != 200:
            abort(r.status_code)
        return r.json()
