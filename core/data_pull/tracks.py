# Import necessary libraries
import logging
import simplejson as json
from datetime import datetime
from connections import client, oauth

# Set-up logging
logging.basicConfig(filename='execute.log', filemode='a', level='INFO')

# Function to be called in other files
def recently_played():
  """Return the recently played tracks API data"""
  # Set-up authorization scope. This is needed since it accesses user data
  scope = 'user-read-recently-played'
  auth_token = oauth(scope=scope)

  # Pull in API data. No need to worry about before/after since that is better handled within SQL
  try:
    results = auth_token.current_user_recently_played(limit=50, after=None, before=None)
  except Exception as err: #TODO: Need to figure out specific exceptions here
    timestamp = datetime.utcnow().replace(microsecond=0)
    error = f"{timestamp} ERROR: Issue gathering recently played data. Message: {err}"
    logging.exception(error) 
  else:
    timestamp = datetime.utcnow().replace(microsecond=0)
    message = f"{timestamp} SUCCESS: Gathered recently played data."
    logging.info(message) 
    try:
      info_json = json.dumps(results, indent=2)
    except ValueError as err:
      timestamp = datetime.utcnow().replace(microsecond=0)
      error = f"{timestamp} ERROR: Issue converting recently played data to JSON. Message: {err}"
      logging.exception(error) 
    else:
      timestamp = datetime.utcnow().replace(microsecond=0)
      message = f"{timestamp} SUCCESS: Converted recently played data to JSON."
      logging.info(message) 
    
  return results, info_json

def track_ids():
  """Gets the track IDs for the recently played tracks"""
  results, _ = recently_played()

  #Loop through each dictionary in the items list to get the track IDs
  tracks = []
  for item in results['items']:
      tracks.append(item['track']['id'])
  
  # De-duplicate the IDs in the list. This prevents downstream functions from
  # hitting the 100 ID limit
  tracks = list(dict.fromkeys(tracks))

  return tracks

def track_features():
  """Return high level features on each recently played track"""
  tracks = track_ids()

  try:
    client_scope = client()
    features = client_scope.audio_features(tracks)
  except Exception as err: #TODO: Need to figure out specific exceptions here
    timestamp = datetime.utcnow().replace(microsecond=0)
    error = f"{timestamp} ERROR: Issue gathering track features data. Message: {err}"
    logging.exception(error) 
  else:
    timestamp = datetime.utcnow().replace(microsecond=0)
    message = f"{timestamp} SUCCESS: Gathered track features data."
    logging.info(message) 
    try:
      features_json = json.dumps(features, indent=2)
    except ValueError as err:
      timestamp = datetime.utcnow().replace(microsecond=0)
      error = f"{timestamp} ERROR: Issue converting track features data to JSON. Message: {err}"
      logging.exception(error) 
    else:
      timestamp = datetime.utcnow().replace(microsecond=0)
      message = f"{timestamp} SUCCESS: Converted track features data to JSON."
      logging.info(message) 

  return features_json
  
def track_analysis():
  """Return granular analysis on each recently played track"""
  tracks = track_ids()

  # Iterate through each track because audio analysis doesn't accept a list of track IDs
  analysis_json = []
  for track in tracks:
    try:
      client_scope = client()
      analysis = client_scope.audio_analysis(track)
      track_clean = "track_id: " + track 
      track_analysis = {track_clean: analysis}
    except Exception as err: #TODO: Need to figure out specific exceptions here
      timestamp = datetime.utcnow().replace(microsecond=0)
      error = f"{timestamp} ERROR: Issue gathering audio analysis data. Message: {err}"
      logging.exception(error) 
    else:
      timestamp = datetime.utcnow().replace(microsecond=0)
      message = f"{timestamp} SUCCESS: Gathered audio analysis data."
      logging.info(message) 
      try:
        single_json = json.dumps(track_analysis, indent=2)
        analysis_json.append(single_json)
      except ValueError as err:
        timestamp = datetime.utcnow().replace(microsecond=0)
        error = f"{timestamp} ERROR: Issue converting audio analysis data to JSON. Message: {err}"
        logging.exception(error) 
      else:
        timestamp = datetime.utcnow().replace(microsecond=0)
        message = f"{timestamp} SUCCESS: Converted audio analysis data to JSON."
        logging.info(message)

  return analysis_json