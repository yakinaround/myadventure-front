"""
controllers.py

Login module controllers.
"""
from flask import Blueprint, render_template, redirect, request, abort, url_for, session
from flask_login import login_user, LoginManager, login_required, logout_user

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
    user = session.get(str(user_id), None)
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

            res = api.get('/user/', token=token)

            user_id = res['user']['_id']
            email = res['user']['email']

            user = User(user_id)
            user.email = email

            session[str(user_id)] = user

            login_user(user)

            next = request.args.get('next')

            if not next_is_valid(next):
                return abort(401)
            return redirect(next or url_for('user.user'))
        return abort(400)
    return render_template('auth/login.html', form=form)


@mod_auth.route("/logout")
@login_required
def logout():
    logout_user()
    next = request.args.get('next')
    return redirect(next or url_for('index.index'))


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
