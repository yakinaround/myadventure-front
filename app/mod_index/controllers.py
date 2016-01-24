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
    return render_template('index.html')


@mod_index.route('/recent')
def recent():
    r = requests.get(_url('/adventure'))
    adventures = r.json()
    return render_template('recent.html', adventures=adventures['adventures'])


@mod_index.route('/signup')
def signup():
    return render_template('signup.html')
