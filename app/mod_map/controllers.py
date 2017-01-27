"""
controllers.py

Map module controllers.
"""
from flask import Blueprint, render_template, current_app

from app.mod_auth.models import MyAdventure

mod_map = Blueprint('map', __name__, url_prefix='/adventure')

api = MyAdventure()


@mod_map.route('/<slug>')
def map(slug):
    adventure = api.get('/adventure/' + slug)
    return render_template('map/index.html', slug=slug, title=adventure['name'] + " | MyAdventure", api_url=current_app.config['API_URL'] + '/api/v1' )
