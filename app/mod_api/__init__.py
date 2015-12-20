"""
Initialize api module

"""

from flask import current_app


def _url(path):
    return current_app.config['API_URL'] + '/api/v1' + path

