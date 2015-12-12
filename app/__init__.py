from flask import Flask, render_template, abort
import os
import requests

from app.mod_api import _url

app = Flask(__name__, static_folder=os.getcwd() + '/app/static', static_url_path='', template_folder=os.getcwd() + '/app/templates')

app.config.from_object('config')


@app.errorhandler(400)
def bad_request(e):
    """Return a custom 400 error."""
    return 'The browser (or proxy) sent a request that this server could not understand.', 400


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def internal_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500


@app.route('/<adventure_slug>')
def map(adventure_slug):
    r = requests.get(_url('/adventure/' + adventure_slug))
    adventure = r.json()
    return render_template('map.html', adventure=adventure_slug, title=adventure['name'], api_url='http://api.myadventure.dev:5000/api/v1')


@app.route('/')
def index():
    return abort(404)

