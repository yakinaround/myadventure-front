"""
controllers.py

User module controllers.
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.mod_auth.models import MyAdventure

mod_user = Blueprint('user', __name__, url_prefix='/user')

api = MyAdventure()


@mod_user.route('/')
@login_required
def user():
    return render_template('user/index.html', user=current_user)
