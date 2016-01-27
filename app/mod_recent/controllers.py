"""
controllers.py

Recent module controllers.
"""
from flask import Blueprint, render_template

from app.mod_auth.models import MyAdventure

mod_recent = Blueprint('recent', __name__, url_prefix='/recent')

api = MyAdventure()


@mod_recent.route('/')
def recent():
    adventures = api.get('/adventure')
    return render_template('recent/index.html', adventures=adventures['adventures'])