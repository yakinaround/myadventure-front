"""
controllers.py

Index module controllers.
"""
import requests
from flask import Blueprint, render_template

from app.mod_api import _url

mod_index = Blueprint('index', __name__, url_prefix='')


@mod_index.route('/')
def index():
    r = requests.get(_url('/adventure'))
    adventures = r.json()
    return render_template('index.html', adventures=adventures['adventures'])
