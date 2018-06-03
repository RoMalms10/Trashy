#!/usr/bin/python3
"""
Flask App that handles API requests and redirects
"""
from flask import Flask, render_template, url_for, redirect, session
from flask import jsonify, request
from flask_login import LoginManager, login_required, login_user, \
    logout_user, current_user
from models import storage, classes
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError
import json

# Flask setup
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.update(SECRET_KEY=classes['Auth'].SECRET_KEY)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"
port = 5000
host = '0.0.0.0'

# Serve html files
@app.route('/')
def landing_page():
    """
    Render the landing page
    """
    return render_template('index.html')

@app.route('/map')
@login_required
def render_map_page():
    """
    Serve the map webpage
    """
    return render_template('map.html')

# API Backend
@app.route('/api/bins')
def get_bins():
    """
    Gets all of the bin info from csv file
    """
    trash_list = []
    obj_dict = storage.all()
    for key, value in obj_dict.items():
        trash_list.append(value.to_dict())
    return jsonify(trash_list)

@app.route('/api/bins/proximity', methods=['POST'])
def proximity_bins():
    """
    Get closest trash cans to user
    returns a dict
    """
    radius = .02
    post_info = request.get_json()
    prox_list = storage.proximity(post_info["latitude"], post_info["longitude"], radius)
    i = 2
    while (len(prox_list) != 20):
        prox_list = storage.proximity(post_info["latitude"], post_info["longitude"], radius*i)
        i = i + 1
    return jsonify(prox_list)

# Google OAuth
@login_manager.user_loader
def load_user(user_id):
    """
    Grabs the user based off the user_id passed
    """
    return storage.g_auth_user_id("User", user_id)

def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(classes["Auth"].CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            classes["Auth"].CLIENT_ID,
            state=state,
            redirect_uri=classes["Auth"].REDIRECT_URI)
    oauth = OAuth2Session(
        classes["Auth"].CLIENT_ID,
        redirect_uri=classes["Auth"].REDIRECT_URI,
        scope=classes["Auth"].SCOPE)
    return oauth

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('render_map_page'))
    google = get_google_auth()
    auth_url, state = google.authorization_url(
        classes["Auth"].AUTH_URI, access_type='offline')
    session['oauth_state'] = state
    return render_template('login.html', auth_url=auth_url)

@app.route('/gCallback')
def callback():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('render_map_page'))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('render_map_page'))
    else:
        google = get_google_auth(state=session['oauth_state'])
        try:
            token = google.fetch_token(
                classes["Auth"].TOKEN_URI,
                client_secret=classes["Auth"].CLIENT_SECRET,
                authorization_response=request.url)
        except HTTPError:
            return 'HTTPError occurred.'
        google = get_google_auth(token=token)
        resp = google.get(classes["Auth"].USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            user = storage.g_auth_user("User", email)
            if user is None:
                user = classes["User"]()
                user.email = email
                user.save()
            user.name = user_data['name']
            print(token)
            user.tokens = json.dumps(token)
            print("before commit")
            storage.save()
            print("after commit")
            login_user(user)
            return redirect(url_for('render_map_page'))
        return 'Could not fetch your information.'

@app.route('/logout')
#@login_required
def logout():
    logout_user()
    return redirect(url_for('landing_page'))

if __name__ == "__main__":
    app.run(host=host, port=port)
