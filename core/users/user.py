"""This will be used to create a user object that can run all of the functions"""

class User:
    """Collects all information needed to pull and load the correct data for each user"""

    def __init__(
        self,
        user_id,
        response_sheet,
        spotify_user,
        spotipy_client_secret,
        spotipy_client_id,
        spotipy_cache
    ):
        """Initialize attributes for Person class"""
        self.user_id = user_id
        self.response_sheet = response_sheet
        self.spotify_user = spotify_user
        self.spotipy_client_secret = spotipy_client_secret
        self.spotipy_client_id = spotipy_client_id
        self.spotipy_cache = spotipy_cache