# Import necessary libraries
import json
from datetime import datetime
import rollbar
from connections import client, oauth  # pylint: disable=import-error
from spotipy.client import SpotifyException

# Function to be called in other files
def recently_played():
    """Return the recently played tracks API data"""
    # Set-up authorization scope. This is needed since it accesses user data
    scope = "user-read-recently-played"
    auth_token = oauth(scope=scope)

    # Pull in API data. No need to worry about before/after since that is better handled within SQL
    try:
        results = auth_token.current_user_recently_played(
            limit=50, after=None, before=None
        )
    except SpotifyException as err:
        timestamp = datetime.utcnow().replace(microsecond=0)
        error = (
            f"{timestamp} ERROR: Issue gathering recently played data. Message: {err}"
        )
        rollbar.report_message(error)
    except Exception:
        rollbar.report_exc_info()
    else:
        # Convert the dictionary to a json object
        try:
            info_json = json.dumps(results, indent=2)
        except ValueError as err:
            timestamp = datetime.utcnow().replace(microsecond=0)
            error = f"{timestamp} ERROR: Issue converting recently played data to JSON. Message: {err}"
            rollbar.report_message(error)
        except Exception:
            rollbar.report_exc_info()

    return results, info_json


def get_ids():
    """Gets the track and artist IDs for the recently played tracks"""

    results, _ = recently_played()
    # Loop through each dictionary in the items list to get the track IDs
    tracks = []
    for item in results["items"]:
        tracks.append(item["track"]["id"])
    artists = []
    for item in results["items"]:
        for artist in item["track"]["artists"]:
            artists.append(artist["id"])
    # De-duplicate the IDs in the list. This prevents downstream functions from
    # hitting the 100 ID limit
    tracks = list(dict.fromkeys(tracks))

    return tracks, artists


def track_features():
    """Return high level features on each recently played track"""
    tracks, _ = get_ids()
    # Pull the API into a dictionary
    try:
        client_scope = client()
        features = client_scope.audio_features(tracks)
    except SpotifyException as err:
        timestamp = datetime.utcnow().replace(microsecond=0)
        error = (
            f"{timestamp} ERROR: Issue gathering track features data. Message: {err}"
        )
        rollbar.report_message(error)
    except Exception:
        rollbar.report_exc_info()
    else:
        # Create a json object from the dictionary
        try:
            features_json = json.dumps(features, indent=2)
        except ValueError as err:
            timestamp = datetime.utcnow().replace(microsecond=0)
            error = f"{timestamp} ERROR: Issue converting track features data to JSON. Message: {err}"
            rollbar.report_message(error)
        except Exception:
            rollbar.report_exc_info()

    return features_json


def track_artists():
    """Bring in the artist-related data tied to the recently played tracks"""

    _, artist_ids = get_ids()
    # Have to limit the number of artists used since there are API limits
    top_artists = artist_ids[:50]
    # Pull the SPI into a dictionary
    try:
        client_scope = client()
        artists = client_scope.artists(top_artists)
    except SpotifyException as err:
        timestamp = datetime.utcnow().replace(microsecond=0)
        error = f"{timestamp} ERROR: Issue gathering track artist data. Message: {err}"
        rollbar.report_message(error)
    except Exception:
        rollbar.report_exc_info()
    else:
        # Create a json object from the dictionary
        try:
            artists_json = json.dumps(artists, indent=2)
        except ValueError as err:
            timestamp = datetime.utcnow().replace(microsecond=0)
            error = f"{timestamp} ERROR: Issue converting track artist data to JSON. Message: {err}"
            rollbar.report_message(error)
        except Exception:
            rollbar.report_exc_info()

    return artists_json
