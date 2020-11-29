# Import necessary libraries
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

# Set-up scope
scope = 'user-read-recently-played'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# Pull in API data
# No need to worry about before/after since that is better handled within SQL
results = sp.current_user_recently_played(limit=50, after=None, before=None)

# Create the json file to pull the stored data
# with open('test.json', 'w',  encoding='utf-8') as outfile: #Need to add encoding to prevent error
#     json.dump(results, outfile, sort_keys=True, ensure_ascii=False, indent=2)

tracks = []
for item in results['items']:
    tracks.append(item['track']['id'])

