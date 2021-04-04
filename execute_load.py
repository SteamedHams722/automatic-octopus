#!/usr/bin/env python3
# pylint: disable=import-error
# This script will pull the API data and load the tables. Eventually, a message
# should be added that provides updates if the run fails

# Import libraries
import sys
import os
import rollbar

# Add folders to path that will be called in other functions. This should be replaced by
# using packages.
home_dir = os.path.expanduser("~")
sys.path.append(os.path.join(home_dir, "core", "storage"))
sys.path.append(os.path.join(home_dir, "core", "message"))
sys.path.append(os.path.join(home_dir, "core", "data_prep"))
sys.path.append(os.path.join(home_dir, "core", "data_pull"))
from load_tracks import tracks_to_pg
from load_responses import responses_to_pg

# Set-up rollbar
rollbar.init(os.getenv("ROLLBAR_ACCESS_TOKEN"))

# Create or overwrite the Spotify Oauth cache file with the cache variable data
# Eventually, this will have to be scaled for each user.


def main():
    """Need to have a function here so Heroku can call it. It will load the postgres tables
    with Spotify data as well as response data. It will also create the Spotipy Cache needed
    to automate the Spotify extract"""
    with open(".cache", "w") as f:
        f.write(os.getenv("SPOTIPY_CACHE"))
    tracks_to_pg()
    responses_to_pg(os.getenv("RESPONSE_SHEET"))


if __name__ == "__main__":
    main()
