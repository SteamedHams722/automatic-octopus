# Import necessary libraries
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import simplejson as json

#Set-up scope
scope = 'user-read-recently-played'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_recently_played(limit=50, after=None, before=None)

json_res = json.dumps(results, sort_keys=True, indent=4 * ' ')

#print(json_res)

# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])

with open('test.txt', 'w') as outfile:
    json.dump(json_res, outfile)