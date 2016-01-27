"""
controllers.py

Facebook module controllers.
"""
from flask import Blueprint, url_for, request, session, Response, redirect, abort
from flask.ext.oauthlib.client import OAuthException
from flask_login import login_user
from flask_oauthlib import client

from app.mod_user.models import User

mod_facebook = Blueprint('facebook', __name__, url_prefix='/facebook')

oauth = client.OAuth()


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

    session['facebook_token'] = (resp['access_token'], '')
    try:
        me = facebook.get('/me?fields=id,name,email,link')
        user = User()
        login_user(user)
    except client.OAuthException:
        return abort(401)

    # client_id = request.args.get('client_id')
    # scope = request.args.get('scope')
    # redirect_uri = request.args.get('redirect_uri')
    # response_type = request.args.get('response_type')

    return redirect(request.args.get('next'))


@mod_facebook.route('/me')
def me():
    me = facebook.get('/me?fields=id,name,email,link')
    return Response('Logged in as id=%s name=%s email=%s redirect=%s' % (me.data.get('id'), me.data.get('name'), me.data.get('email'), request.args.get('next')))
