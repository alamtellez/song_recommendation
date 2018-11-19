import pprint
import os
import sys
import json
import webbrowser
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
from env import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

username = 'ferminamc'
scope = 'user-library-read'
client_id = SPOTIPY_CLIENT_ID
client_secret = SPOTIPY_CLIENT_SECRET
redirect_uri = SPOTIPY_REDIRECT_URI

# Get access token and delete cache in case it fails
try:
    token = util.prompt_for_user_token(username,scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username,scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)

# Create a Spotify object
col_names = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness']
if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        track_id = track['id']
        pprint.pprint(sp.audio_features(track_id)[0]['acousticness'])
        break
        #print(track['name'] + ' - ' + track['artists'][0]['name'])
else:
    print("Can't get token for", username)
