import json
import requests

from collections import defaultdict
from flask import Blueprint
from numpy import mean


artists = Blueprint('artists', __name__)

@artists.route('/<artist_id>')
def get_album_data(artist_id):
  try:
    def get_data(artist_id):
      artist_url = "http://ws.spotify.com/lookup/1/.json" + \
                   "?uri=spotify:artist:%s&extras=albumdetail" % artist_id
      artist_resp = requests.get(artist_url).json()
      artist_name = artist_resp['artist']['name']
      albums = []
      album_names = set()
      for album in artist_resp['artist']['albums']:
        name = album['album']['name']
        if name not in album_names:
          album_names.add(name)
          album_id = album['album']['href'].replace('spotify:album:', '')
          album_url = "http://ws.spotify.com/lookup/1/.json" + \
                      "?uri=spotify:album:%s&extras=trackdetail" % album_id
          year = album['album']['released']
          album_resp = requests.get(album_url).json()
          track_pops = []
          for track in album_resp['album']['tracks']:
            track_pops.append(float(track['popularity']))

          albums.append({
            'name': name,
            'year': year,
            'pop':  round(mean(track_pops), 3),
          })

      return artist_name, albums

    artist_name, albums = get_data(artist_id)

    pops = [(a['pop']) for a in albums]
    pop_max = max(pops)
    pop_min = min(pops)
    pop_range = pop_max - pop_min
    pop_sum = sum(pops)
    rel_pop_sum = sum([(pop - pop_min) / pop_range for pop in pops])

    for album in albums:
      album['rel_pop'] = round((album['pop'] - pop_min) / pop_range, 3)

    album_data = sorted(albums, key=lambda a: a['year'])

    return json.dumps({
      'artist': artist_name,
      'albums': album_data,
    })
  except Exception as e:
    print 'error', e
