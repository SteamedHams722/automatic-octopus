# Import necessary libraries
import simplejson as json
import spotipy
import sys
from connections import oauth, client

# Function to be called in other files
def recently_played():
    """Return the recently played tracks API data"""
    # Set-up authorization scope. This is needed since it accesses user data
    scope = 'user-read-recently-played'
    auth_scope = oauth(scope=scope)

    # Pull in API data. No need to worry about before/after since that is better handled within SQL
    results = auth_scope.current_user_recently_played(limit=50, after=None, before=None)
    info_json = json.dumps(recently_played(), indent=2)

    return results, info_json

def track_ids():
    """Gets the track IDs for the recently played tracks"""
    results, _ = recently_played()

    #Loop through each dictionary in the items list to get the track IDs
    tracks = []
    for item in results['items']:
        tracks.append(item['track']['id'])
    
    # De-duplicate the IDs in the list. This prevents downstream functions from
    # hitting the 100 ID limit
    tracks = list(dict.fromkeys(tracks))

    return tracks

def track_features():
    """Return high level features on each recently played track"""
    tracks = track_ids()
    client_scope = client()
    track_features = client_scope.audio_features(tracks)
    features_json = json.dumps(track_features, indent=2)

    return features_json