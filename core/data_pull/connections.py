# This will store the connection information for both the authorization and
# client credentials options

# Import necessary libraries
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException #Will need this for exception handling

# Set up OAuth function
def oauth(scope, auth_manager=SpotifyOAuth):
    '''Return the OAuth information needed to access user data'''
    oauth_conn = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    return oauth_conn

def client(auth_manager=SpotifyClientCredentials):
    '''Return the client credentials needed to access non-user data'''
    auth_manager = SpotifyClientCredentials()
    client_conn = spotipy.Spotify(auth_manager=auth_manager)

    return client_conn

