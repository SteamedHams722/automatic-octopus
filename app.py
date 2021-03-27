'''Simple script to create the cache file needed for authentication'''
import os

#Create or overwrite the cache file with the cache variable data
#Eventually, this will have to be scaled for each user.
with open('.cache', 'w') as f:
    f.write(os.getenv('SPOTIPY_CACHE'))