"""
controllers.py

Login module controllers.
"""
import logging
from flask import Blueprint, render_template, redirect, request, abort, url_for
from flask_login import login_user, LoginManager

from app.mod_login.models import LoginForm
from app.mod_user import get_user

mod_login = Blueprint('login', __name__, url_prefix='')

login_manager = LoginManager()


def next_is_valid(next):
    return True


@mod_login.record_once
def on_load(state):
    login_manager.init_app(state.app)


@login_manager.user_loader
def user_loader(email):
    user = get_user(email)
    return user


@mod_login.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = request.form.get('email')
            user = get_user(email)

            if user.is_authenticated:
                login_user(user)

                next = request.args.get('next')

                if not next_is_valid(next):
                    return abort(401)
                return redirect(next or url_for('index.index'))
            return abort(401)
        return abort(400)
    return render_template('login.html', form=form)
