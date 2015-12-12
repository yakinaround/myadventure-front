"""
controllers.py

API module controllers.
"""
from flask import Blueprint, url_for, request, current_app, session, jsonify
from flask_oauthlib import client

mod_api = Blueprint('api', __name__, url_prefix='')

oauth = client.OAuth(current_app)

CLIENT_ID = '1EssHrEXtGdmJHFQ2YEU1leNsHljVPZp1RmRsYDZ'
CLIENT_SECRET = 'WtAikOHT38puo0FHhNrqYbCi6shLFSJjsmc2KVsms8i7utni1h'

remote = oauth.remote_app(
    'remote',
    consumer_key=CLIENT_ID,
    consumer_secret=CLIENT_SECRET,
    request_token_params={'scope': 'email'},
    base_url='http://api.myadventure.dev:5000/api/v1',
    request_token_url=None,
    access_token_url='http://api.myadventure.dev:5000/oauth/token',
    authorize_url='http://api.myadventure.dev:5000/oauth/authorize',
    access_token_method='POST'
)


@mod_api.route('/login')
def index():
    if 'remote_oauth' in session:
        resp = remote.get('/user')
        if resp.status != 401:
            return jsonify(resp.data)
    next_url = request.args.get('next') or request.referrer or None
    return remote.authorize(
        callback=url_for('authorized', next=next_url, _external=True)
    )


@mod_api.route('/authorized')
def authorized():
    resp = remote.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['remote_oauth'] = (resp['access_token'], '')
    return jsonify(oauth_token=resp['access_token'])


@remote.tokengetter
def get_oauth_token():
    return session.get('remote_oauth')




