"""
controllers.py

Index module controllers.
"""
from flask import Blueprint, render_template

from app.mod_api.models import MyAdventure

mod_index = Blueprint('index', __name__, url_prefix='')

api = MyAdventure()


@mod_index.route('/')
def index():
    return render_template('index.html')


@mod_index.route('/recent')
def recent():
    adventures = api.get('/adventure')
    return render_template('recent.html', adventures=adventures['adventures'])
