from flask import Flask, request, url_for, session, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from time import gmtime, strftime
from credentials import CLIENT_ID, CLIENT_SECRET, SECRET_KEY
import os
import datetime
from flask import jsonify
import predict as pred

# Defining consts
TOKEN_CODE = "token_info"


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=url_for("redirectPage", _external=True),
        scope="user-top-read user-library-read user-read-playback-state user-modify-playback-state"
    )


app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SESSION_COOKIE_NAME'] = 'New Cookie'


@app.route('/')
def index():
    name = 'username'
    return render_template('index.html', title='Welcome', username=name)


@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/redirectPage')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_CODE] = token_info
    return redirect(url_for("getTracks", _external=True))


def get_token():
    token_info = session.get(TOKEN_CODE, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect("/")
    sp = spotipy.Spotify(
        auth=token_info['access_token'],
    )

    current_user_name = sp.current_user()['display_name']
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365)

    # Set the genre that you want to fetch the top songs for

    try:
        predicted = pred.get_emotion()
    except:
        predicted = 'happy'
    if predicted == 'happy':
        genre = "pop"
    if predicted == 'sad':
        genre = "blues"
    if predicted == 'angry':
        genre = "rock"
    if predicted == 'relaxed':
        genre = "chill-out"

    # Use the search() method to get a list of tracks matching the given genre
    results = sp.search(q=f"genre:{genre}", type="track", limit=10)

    tracks = []
    for track in results['tracks']['items']:
        track_info = {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'duration_ms': track['duration_ms'],
            'preview_url': track['preview_url']
        }
        tracks.append(track_info)

    if os.path.exists(".cache"):
        os.remove(".cache")
    # Render template with track information
    return render_template('music.html', tracks=tracks, emotion=predicted)
    # return jsonify(tracks)


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    return strftime("%a, %d %b %Y", date)


@app.template_filter('mmss')
def _jinja2_filter_miliseconds(time, fmt=None):
    time = int(time / 1000)
    minutes = time // 60
    seconds = time % 60
    if seconds < 10:
        return str(minutes) + ":0" + str(seconds)
    return str(minutes) + ":" + str(seconds)
