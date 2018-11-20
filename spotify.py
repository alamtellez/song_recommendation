import pprint
import random
import csv
import os
import sys
import json
import webbrowser
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
from env import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

import numpy as np
import pandas
from sklearn.neural_network import MLPClassifier

def get_token():
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

    return token

# Creates a CSV file with songs I like and dislike for later use
def get_train_data():
    token = get_token()
    username = 'ferminamc'

    col_names = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'liked']
    train_data = []
    train_data.append(col_names)
    repeat = 3
    limit = 20 # Number of songs that will be downloaded
    if token:
        sp = spotipy.Spotify(auth=token)
        # Get 100 liked songs
        for i in range(repeat):
            results = sp.current_user_saved_tracks(offset=(i*limit))
            for item in results['items']:
                temp_data = []
                track_id = item['track']['id']
                track_features = sp.audio_features(track_id)
                for col in col_names[0:-1]:
                    temp_data.append(track_features[0][col])
                temp_data.append(1)
                train_data.append(temp_data)

        # K-pop playlist
        k_pop_user = 'spotify'
        k_pop_playlist = '37i9dQZF1DX9tPFwDMOaN1?si=EIk4w9gVTImLOHtRfvqY8g'
        # Getting songs I don't like for the training
        results = sp.user_playlist(k_pop_user, k_pop_playlist)
        for item in results['tracks']['items']:
            temp_data = []
            track_id = item['track']['id']
            track_features = sp.audio_features(track_id)
            for col in col_names[0:-1]:
                temp_data.append(track_features[0][col])
            temp_data.append(0)
            train_data.append(temp_data)
        # Global Top 50
        top_50_user = 'spotifycharts'
        top_50_playlist = '37i9dQZEVXbMDoHDwVN2tF'
        results = sp.user_playlist(top_50_user, top_50_playlist)
        for item in results['tracks']['items']:
            temp_data = []
            track_id = item['track']['id']
            track_features = sp.audio_features(track_id)
            for col in col_names[0:-1]:
                temp_data.append(track_features[0][col])
            temp_data.append(random.uniform(0.4, 0.6))
            train_data.append(temp_data)
    else:
        print("Can't get token for", username)

    with open('train_data.csv', 'w', newline='') as csvfile:
        write_csv = csv.writer(csvfile)
        write_csv.writerow(train_data[0])
        for row in train_data[1:]:
            write_csv.writerow(row)

def get_test_data():
    username = 'ferminamc'
    token = get_token()
    col_names = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness']
    test_data = []
    test_data.append(col_names)

    if token:
        sp = spotipy.Spotify(auth=token)
        weekly_recommendation_user = 'spotify'
        weekly_recommendation_playlist = '37i9dQZEVXcO15uASmzVtt'
        results = sp.user_playlist(weekly_recommendation_user, weekly_recommendation_playlist)
        for item in results['tracks']['items']:
            temp_data = []
            track_id = item['track']['id']
            track_features = sp.audio_features(track_id)
            for col in col_names[0:-1]:
                temp_data.append(track_features[0][col])
            test_data.append(temp_data)
    else:
        print("Can't get token for", username)

    with open('test_data.csv', 'w', newline='') as csvfile:
        write_csv = csv.writer(csvfile)
        write_csv.writerow(test_data[0])
        for row in test_data[1:]:
            write_csv.writerow(row)
