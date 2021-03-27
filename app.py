'''This is just a placeholder app for establishing the dynos'''

#Add this code here:
import os
from flask import Flask

# Create the Spotipy cache file if it doesn't exist
if not os.path.exists('.cache'):
    with open('.cache', 'w') as f:
        f.write(os.getenv('SPOTIPY_CACHE'))

app = Flask(__name__)

@app.route('/')
def index():
    return 'Champions of Winning, Superb!'

if __name__ == "__main__":
    app.run(os.getenv('PORT'))