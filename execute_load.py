#!/usr/bin/env python3
# pylint: disable=import-error
# This script will pull the API data and load the tables. Eventually, a message
# should be added that provides updates if the run fails

# Import libraries
import sys
import os
from datetime import datetime
import rollbar

# Add folders to path that will be called in other functions. This should be replaced by
# using packages.
user_home = os.path.expanduser("~")
sys.path.append(os.path.join(user_home, "core", "storage"))
sys.path.append(os.path.join(user_home, "core", "message"))
sys.path.append(os.path.join(user_home, "core", "data_prep"))
sys.path.append(os.path.join(user_home, "core", "data_pull"))
from load_tracks import tracks_to_pg
from load_responses import responses_to_pg
from transmit import communicado

# Set-up rollbar
rollbar.init(os.getenv("ROLLBAR_ACCESS_TOKEN"))

# Create or overwrite the Spotify Oauth cache file with the cache variable data
# Eventually, this will have to be scaled for each user.
with open(".cache", "w") as f:
    f.write(os.getenv("SPOTIPY_CACHE"))


def load_all():
    """Need to have a function here so Heroku can call it. I'm currently excluding the
    response calls since it is not working correctly on raspberry pi."""
    # Load the tables and send a text message if it fails
    success_dict = {
        "tracks": tracks_to_pg(),
        "responses": responses_to_pg(os.getenv("response_sheet")),
    }
    for key, val in success_dict.items():
        try:
            if val:  # A True value means the job succeeded.
                # communicado(table_group=key, success=val) #This is only needed for testing.
                timestamp = datetime.utcnow().replace(microsecond=0)
                message = f" {timestamp} No message sent. Data load jobs succeeded."
            else:
                communicado(table_group=key, success=val)
                timestamp = datetime.utcnow().replace(microsecond=0)
                message = f" {timestamp} Failure message sent. There was an issue when trying to load data"
                raise ValueError(message)  # Want a specific exception for this failure
        except ValueError as err:
            rollbar.report_message(err)
        except Exception:
            # Catch-all
            rollbar.report_exc_info()


def main():
    """Main executable for the code"""
    load_all()


if __name__ == "__main__":
    main()
