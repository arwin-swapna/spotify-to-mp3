import csv
import os
import urllib.request
import re
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect, render_template
from pytube import YouTube
from moviepy.editor import *

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = os.getenv("SECRET_KEY")
TOKEN_INFO = 'token_info'

# Function to create a SpotifyOAuth object
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=url_for('redirect_page', _external=True),
        scope='user-library-read playlist-modify-public playlist-modify-private'
    )

@app.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return render_template('login.html', auth_url=auth_url)

@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('save_discover_weekly', _external=True))

@app.route('/saveDiscoverWeekly')
def save_discover_weekly():
    try:
        token_info = get_token()
    except:
        print('User not logged in')
        return redirect("/")

    sp = spotipy.Spotify(auth=token_info['access_token'])

    current_playlists = sp.current_user_playlists()['items']
    spotify_scam_id = None
    saved_weekly_playlist_id = None

    for playlist in current_playlists:
        if playlist['name'] == 'spotifyscam':
            spotify_scam_id = playlist['id']

    if not spotify_scam_id:
        return "Scam playlist not found"

    scamPlaylist = sp.playlist_items(spotify_scam_id)

    # Prepare data for rendering in the template
    song_details = []
    for song in scamPlaylist['items']:
        track_name = song['track']['name']
        string_without_spaces = re.sub(r'\s', '', track_name)
        search_keyword = string_without_spaces
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        song_details.append({'track_name': track_name, 'link': "https://www.youtube.com/watch?v=" + video_ids[0]})
    
    for savedSong in song_details:
        
        url = savedSong['link']

        # Download the video
        try:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            stream.download()

            video_title = yt.title.replace(".", "")
            print(stream.title, video_title)
            # Extract the audio
            video = VideoFileClip(video_title+'.mp4')
            audio = video.audio
            audio.write_audiofile(video_title+'.mp3')
            video.close()
        except:
            continue
        # Delete the downloaded video file
        

        retries = 0
        max_retries = 5
        while retries < max_retries:
            try:
                os.remove(video_title+'.mp4')
                break  # Download succeeded, exit the loop
            except PermissionError:
                print(f"File is in use. Retrying in {3} seconds...")
                time.sleep(3)
                retries += 1

    return render_template('save_discover_weekly.html', song_details=song_details)

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for('login', _external=False))

    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

if __name__ == '__main__':
    app.run(debug=True)
