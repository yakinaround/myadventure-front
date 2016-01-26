"""
controllers.py

Login module controllers.
"""
import logging
from flask import Blueprint, render_template, redirect, request, abort, url_for, current_app
from flask_login import login_user, LoginManager

from app.mod_login.models import LoginForm
from app.mod_user import get_user


mod_login = Blueprint('login', __name__, url_prefix='')

login_manager = None


def next_is_valid(next):
    return True


@mod_login.before_app_first_request
def init_login_manager():
    global login_manager
    login_manager = LoginManager()
    login_manager.init_app(current_app)

    @login_manager.user_loader
    def user_loader(email):
        user = get_user(email)
        return user


@mod_login.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm()
        if form.validate_on_submit():
            email = request.form.get('email')
            user = get_user(email)

            if user.is_authenticated:
                remember = form.remember.data
                login_user(user, remember=remember)

                next = request.args.get('next')

                if not next_is_valid(next):
                    return abort(401)

                logging.error("success")
                return redirect(next or url_for('index.index'))
            return abort(401)
        return abort(400)
    return render_template('login.html')