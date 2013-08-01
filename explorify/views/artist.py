import json
import requests

from collections import defaultdict
from flask import Blueprint


artists = Blueprint('artists', __name__)

@artists.route('/<artist_id>')
def get_album_data(artist_id):
  try:
    artist_url = "http://ws.spotify.com/lookup/1/.json" + \
                 "?uri=spotify:artist:%s&extras=albumdetail" % artist_id
    artist_resp = requests.get(artist_url).json()
    albums = defaultdict(list)
    for album in artist_resp['artist']['albums']:
      album_id = album['album']['href'].replace('spotify:album:', '')
      album_url = "http://ws.spotify.com/lookup/1/.json" + \
                  "?uri=spotify:album:%s&extras=trackdetail" % album_id
      album_resp = requests.get(album_url).json()
      for track in album_resp['album']['tracks']:
        albums[album['album']['name']].append(track['name'])

    return '{}'
  except Exception as e:
    print 'error', e
