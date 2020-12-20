import simplejson as json
from track_info import track_ids
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from connections import client
#Set up the client credentials flow. This flow is fine since no user data is accessed.
conn = client()

#Create a variable that stores the recently played track list
tracks = track_ids()

def track_features():
    """Return high level features on each recently played track"""
    client_scope = client()
    track_features = client_scope.audio_features(tracks)
    features_json = json.dumps(track_features, indent=2)

    return features_json