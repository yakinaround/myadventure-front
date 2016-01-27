"""
controllers.py

Facebook module controllers.
"""
from flask import Blueprint, url_for, request, session, redirect, abort
from flask_login import login_user
from flask.ext.oauthlib.client import OAuthException
from flask_oauthlib import client

from app.mod_user.models import User
from app.mod_auth.models import MyAdventure

mod_facebook = Blueprint('facebook', __name__, url_prefix='/facebook')

oauth = client.OAuth()
api = MyAdventure()


@mod_facebook.record_once
def on_load(state):
    global facebook

    oauth.init_app(state.app)

    facebook = oauth.remote_app(
        'facebook',
        consumer_key=state.app.config['FACEBOOK_APP_ID'],
        consumer_secret=state.app.config['FACEBOOK_APP_SECRET'],
        request_token_params={'scope': 'email'},
        base_url='https://graph.facebook.com',
        request_token_url=None,
        access_token_url='/oauth/access_token',
        access_token_method='GET',
        authorize_url='https://www.facebook.com/dialog/oauth'
    )

    @facebook.tokengetter
    def get_facebook_oauth_token():
        return session.get('facebook_token')


@mod_facebook.route('/login')
def login():
    callback = url_for(
        'facebook.facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return facebook.authorize(callback=callback)


@mod_facebook.route('/login/authorized')
def facebook_authorized():
    resp = facebook.authorized_response()
    if resp is None:
        # return 'Access denied: reason=%s error=%s' % (
        #     request.args['error_reason'],
        #     request.args['error_description']
        # )
        return abort(401)
    if isinstance(resp, OAuthException):
        # return 'Access denied: %s' % resp.message
        return abort(401)

    access_token = resp['access_token']

    session['facebook_token'] = (access_token, '')
    try:
        me = facebook.get('/me?fields=id')
        facebook_id = me.data['id']

        token = api.get_token(facebook_id, access_token)['access_token']

        res = api.get('/user/', token=token)

        user_id = res['user']['_id']
        email = res['user']['email']

        user = User(user_id)
        user.email = email

        login_user(user)
        session[str(user_id)] = user
    except client.OAuthException:
        return abort(401)

    # client_id = request.args.get('client_id')
    # scope = request.args.get('scope')
    # redirect_uri = request.args.get('redirect_uri')
    # response_type = request.args.get('response_type')

    return redirect(request.args.get('next'))

