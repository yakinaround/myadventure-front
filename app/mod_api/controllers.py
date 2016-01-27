"""
controllers.py

API module controllers.
"""
from flask import Blueprint, url_for, request, session, jsonify
from flask_oauthlib import client

mod_api = Blueprint('api', __name__, url_prefix='/api')

oauth = client.OAuth()


@mod_api.record_once
def on_load(state):
    global remote

    oauth.init_app(state.app)
    remote = oauth.remote_app(
        'remote',
        consumer_key=state.app.config['API_CLIENT_ID'],
        consumer_secret=state.app.config['API_CLIENT_SECRET'],
        request_token_params={'scope': 'email'},
        base_url=state.app.config['API_URL'] + '/api/v1',
        request_token_url=None,
        access_token_url=state.app.config['API_URL'] + '/oauth/token',
        authorize_url=state.app.config['API_URL'] + '/oauth/authorize',
        access_token_method='POST'
    )

    @remote.tokengetter
    def get_oauth_token():
        return session.get('remote_token')


@mod_api.route('/login')
def login():
    if 'remote_token' in session:
        resp = remote.get('/api/v1/user')
        if resp.status != 401:
            return jsonify(resp.data)
    # next_url = request.args.get('next') or request.referrer or None
    return remote.authorize(
        callback=url_for('.authorized', _external=True)
    )


@mod_api.route('/authorized')
def authorized():
    resp = remote.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['remote_token'] = (resp['access_token'], '')
    return jsonify(remote_token=resp['access_token'])
