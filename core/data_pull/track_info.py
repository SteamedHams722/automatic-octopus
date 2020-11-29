# Import necessary libraries
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Function to be called in other files
def recently_played():
    """Return the recently played tracks API data"""

    # Set-up authorization scope. This is needed since it accesses user data
    scope = 'user-read-recently-played'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # Pull in API data
    # No need to worry about before/after since that is better handled within SQL
    results = sp.current_user_recently_played(limit=50, after=None, before=None)

    return results

def track_ids():
    """Gets the track IDs for the recently played tracks"""

    #Get the json object from the previous function
    results = recently_played()

    #Loop through each dictionary in the items list to get the track IDs
    tracks = []
    for item in results['items']:
        tracks.append(item['track']['id'])
    
    # De-duplicate the IDs in the list. This prevents downstream functions from
    # hitting the 100 ID limit
    tracks = list(dict.fromkeys(tracks))

    return tracks




