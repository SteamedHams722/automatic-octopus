from track_info import track_ids
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from connections import client
import json

#Set up the client credentials flow. This flow is fine since no user data is accessed.
conn = client()

#Create a variable that stores the recently played track list
tracks = track_ids()

def features():
    """Return high level features on each recently played track"""
    client_scope = client()
    track_features = client_scope.audio_features(tracks)

    return track_features

test = features()

print(test)