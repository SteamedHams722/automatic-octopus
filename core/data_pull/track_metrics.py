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

def analysis():
    """Return detailed audio analysis of each recently played track. Since a for loop
    is required, this will cause ~50 calls to the API so it's probably best not
    to use this function unless the data proves to be valuable"""

    #A list of IDs can't be used so the audio analysis data needs to be iterated 
    # for each ID, create an ID/analysis dictionary, and add it to a list of all 
    # the analysis dictionaries
    analyses = []
    for track_id in tracks:
        track_analysis = sp.audio_analysis(track_id)
        analysis_dict = {track_id: track_analysis}
        analyses.append(analysis_dict)
    
    return analyses