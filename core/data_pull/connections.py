# This will store the connection information for both the authorization and
# client credentials options

# Import necessary libraries
from datetime import datetime
import logging
from urllib3.exceptions import NewConnectionError, MaxRetryError, ConnectTimeoutError
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials, SpotifyOauthError

# Set-up logging
logging.basicConfig(filename='execute.log', filemode='a', level='INFO')

#Set up client credentials needed for basic info
def client():
    '''Return the client credentials needed to access non-user data'''
    try:
        client_conn = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    except (NewConnectionError, MaxRetryError, ConnectTimeoutError) as err:
        timestamp = datetime.utcnow().replace(microsecond=0)
        error = f" {timestamp} ERROR: There was an issue establishing the client credentials. Message: {err}"
        logging.exception(error)
    else:
        timestamp = datetime.utcnow().replace(microsecond=0)
        message = f"{timestamp} SUCCESS: The client credentials were established."
        logging.info(message)

    return client_conn

# Set up OAuth functions for user-specific info
def oauth(scope):
    '''Return the OAuth information needed to access user data and refresh the
    token as needed.'''
    #Get the base authentication connection
    sp_oauth = SpotifyOAuth(scope=scope)

    #Set-up a token refresh so users don't have to log in constantly
    token_info = sp_oauth.get_cached_token() 
    try:
        if token_info:
            token = token_info['access_token']
        else:
            auth_url = sp_oauth.get_authorize_url()
            print(auth_url)
            response = input('Paste the above link into your browser, then paste the redirect url here: ')
            code = sp_oauth.parse_response_code(response)
            token_info = sp_oauth.get_access_token(code)
            token = token_info['access_token']

        sp = spotipy.Spotify(auth=token)
    except (MaxRetryError, NewConnectionError, ConnectTimeoutError, SpotifyOauthError) as err:
        timestamp = datetime.utcnow().replace(microsecond=0)
        error = f" {timestamp} ERROR: There was an issue acquiring the access token. Message: {err}"
        logging.exception(error)
    else:
        timestamp = datetime.utcnow().replace(microsecond=0)
        message = f"{timestamp} SUCCESS: The access token exists"
        logging.info(message)

    # Refresh the access token if it is expired
    try:
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            token = token_info['access_token']
            auth_token = spotipy.Spotify(auth=token)
        else:
            auth_token = sp
    except (MaxRetryError, NewConnectionError, ConnectTimeoutError, SpotifyOauthError) as err:
        timestamp = datetime.utcnow().replace(microsecond=0)
        error = f" {timestamp} ERROR: There was an issue refreshing the access token. Message: {err}"
        logging.exception(error)
    else:
        timestamp = datetime.utcnow().replace(microsecond=0)
        message = f"{timestamp} SUCCESS: The access token was refreshed."
        logging.info(message)

    return auth_token



