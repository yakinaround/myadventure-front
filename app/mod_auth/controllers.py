"""
controllers.py

Login module controllers.
"""
from flask import Blueprint, render_template, redirect, request, abort, url_for
from flask_login import login_user, LoginManager
from werkzeug.exceptions import Unauthorized

from app.mod_auth.models import MyAdventure
from app.mod_user.models import User
from .forms import LoginForm

mod_auth = Blueprint('auth', __name__, url_prefix='')

login_manager = LoginManager()

api = MyAdventure()


def next_is_valid(next):
    return True


@login_manager.user_loader
def user_loader(user_id):
    try:
        user = User(user_id)
    except Unauthorized:
        return None
    return user


@mod_auth.record_once
def on_load(state):
    login_manager.init_app(state.app)
    login_manager.login_view = 'auth.login'


@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = request.form.get('email')
            password = request.form.get('password')

            token = api.get_token(email, password)['access_token']

            user = User(token)
            login_user(user)

            next = request.args.get('next')

            if not next_is_valid(next):
                return abort(401)
            return redirect(next or url_for('user.user'))
        return abort(400)
    return render_template('auth/login.html', form=form)


@mod_auth.route('/signup', methods=['POST'])
def signup():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')

        api.post('/user/', {"email": email, "password": password})

        next = request.args.get('next')

        return redirect(url_for('.login'), code=307, next=next)
    return abort(400)
