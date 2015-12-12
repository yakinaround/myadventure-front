"""
controllers.py

Index module controllers.
"""
from flask import Blueprint, abort

mod_index = Blueprint('index', __name__, url_prefix='')


@mod_index.route('/')
def index():
    return abort(404)
