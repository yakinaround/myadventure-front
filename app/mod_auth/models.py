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
    def get(path, token=None):
        headers = {}
        if token:
            headers['Authorization'] = 'Bearer {}'.format(token)
        r = requests.get(current_app.config['API_URL'] + '/api/v1' + path, headers=headers)
        if r.status_code != 200:
            abort(r.status_code)
        return r.json()

    @staticmethod
    def post(path, data):
        r = requests.post(current_app.config['API_URL'] + '/api/v1' + path, data=data)
        if r.status_code != 200:
            return abort(r.status_code)
        return r.json()

    @staticmethod
    def get_token(username, password):
        data = {"client_id": current_app.config['API_CLIENT_ID'], "grant_type": "password", "username": username, "password": password}
        r = requests.post(current_app.config['API_URL'] + '/oauth/token', data=data)
        if r.status_code != 200:
            abort(r.status_code)
        return r.json()
