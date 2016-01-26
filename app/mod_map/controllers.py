"""
controllers.py

Map module controllers.
"""
import requests
from flask import Blueprint, render_template, abort

from app.mod_api.models import MyAdventure

mod_map = Blueprint('map', __name__, url_prefix='')

api = MyAdventure()


@mod_map.route('/<adventure_slug>')
def map(adventure_slug):
    adventure = api.get('/adventure/' + adventure_slug)
    return render_template('map.html', adventure=adventure_slug, title=adventure['name'] + " - MyAdventure", api_url=_url(''))
