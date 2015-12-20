"""
controllers.py

Map module controllers.
"""
import requests
from flask import Blueprint, render_template, abort

from app.mod_api import _url

mod_map = Blueprint('map', __name__, url_prefix='')


@mod_map.route('/<adventure_slug>')
def map(adventure_slug):
    r = requests.get(_url('/adventure/' + adventure_slug))
    if r.status_code == 404:
        abort(404)
    adventure = r.json()
    return render_template('map.html', adventure=adventure_slug, title=adventure['name'], api_url='http://api.myadventure.dev:5000/api/v1')