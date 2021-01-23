# This will store the connection information for both the authorization and
# client credentials options

# Import necessary libraries
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

#Set up client credentials needed for basic info
def client():
    '''Return the client credentials needed to access non-user data'''
    client_conn = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

    return client_conn

# Set up OAuth functions for user-specific info
def oauth(scope):
    '''Return the OAuth information needed to access user data and refresh the
    token as needed.'''
    #Get the base authentication connection
    sp_oauth = SpotifyOAuth(scope=scope)
    oauth_conn = spotipy.Spotify(auth_manager=sp_oauth)

    #Set-up a token refresh so users don't have to log in constantly
    token_info = sp_oauth.get_cached_token() 
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        print(auth_url)
        response = input('Paste the above link into your browser, then paste the redirect url here: ')

        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code)

        token = token_info['access_token']

    return oauth_conn, token

conn, token = oauth(scope='user-read-recently-played')

print(token)