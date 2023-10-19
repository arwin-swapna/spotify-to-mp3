import csv
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'SDFGSDF5423543ujkhkjh123%$^&%^&'
TOKEN_INFO = 'token_info'

@app.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('save_discover_weekly',_external=True))

@app.route('/saveDiscoverWeekly')
def save_discover_weekly():
    try: 
        token_info = get_token()
    except:
        print('User not logged in')
        return redirect("/")

    sp = spotipy.Spotify(auth=token_info['access_token'])

    current_playlists =  sp.current_user_playlists()['items']
    spotify_scam_id = None
    saved_weekly_playlist_id = None

    for playlist in current_playlists:
        if playlist['name'] == 'spotifyscam':
            spotify_scam_id = playlist['id']

    if not spotify_scam_id:
        return "Scam playlist not found"
    
    scamPlaylist = sp.playlist_items(spotify_scam_id)

    with open('playlists.csv', "a", newline="") as csv_file:
        # Create a CSV writer
        csv_writer = csv.writer(csv_file)

        # Write the headers (if needed)
        # csv_writer.writerow(["Track Name", "Artist Name", "Album Name"])  # Uncomment this line if you want headers

        for song in scamPlaylist['items']:
            track_name = song['track']['name']
            artist_name = song['track']['artists'][0]['name']  # Assuming there is only one artist
            album_name = song['track']['album']['name']
            csv_writer.writerow([track_name, artist_name, album_name])

    return 'Successfully saved song details from "spotifyscam" playlist to CSV file'



def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for('login', _external=False))
    
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = '0d8706cb19c748f0ab71ffe4debdb081',
        client_secret = '62efa5d166734906aa692e11aa62194f',
        redirect_uri = url_for('redirect_page', _external=True),
        scope='user-library-read playlist-modify-public playlist-modify-private'
    )

app.run(debug=True)
