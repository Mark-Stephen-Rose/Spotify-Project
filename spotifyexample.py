from flask import Flask, redirect, request, session, url_for
from spotipy.oauth2 import SpotifyOAuth
import os
import spotipy

app = Flask(__name__)

os.environ['SPOTIPY_CLIENT_ID'] = 'f39**********************'
os.environ['SPOTIPY_CLIENT_SECRET'] = '800**********************'
os.environ['SPOTIPY_REDIRECT_URI'] = 'https://collectparking-spoonfinal-8000.codio.io/callback'

# Scopes define the permissions your app will have
scope = 'user-read-email' 

@app.route('/')
def login():
    sp_oauth = SpotifyOAuth(scope=scope)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = SpotifyOAuth(scope=scope)
    session['token_info'] = sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_data'))

@app.route('/get_data')
def get_data():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    current_user = sp.current_user()
    return current_user


if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(host='0.0.0.0', port=8000, threaded=True, debug=True)
