# Import necessary libraries
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Function to be called in other files
def recently_played():
    """Return the recently played tracks API data"""

    # Set-up scope
    scope = 'user-read-recently-played'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # Pull in API data
    # No need to worry about before/after since that is better handled within SQL
    results = sp.current_user_recently_played(limit=50, after=None, before=None)

    return results




