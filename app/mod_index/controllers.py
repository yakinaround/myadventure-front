"""
controllers.py

Index module controllers.
"""
from flask import Blueprint, render_template

mod_index = Blueprint('index', __name__, url_prefix='')


@mod_index.route('/')
def index():
    return render_template('index.html')

