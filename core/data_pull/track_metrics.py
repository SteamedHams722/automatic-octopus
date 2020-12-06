from track_info import track_ids
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

#Set up the client credentials flow. This flow is fine since no user data is accessed.
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

#Create a variable that stores the recently played track list
tracks = track_ids()

def features():
    """Return high level features on each recently played track"""

    # Pull in API data for features
    track_features = sp.audio_features(tracks)

    return track_features