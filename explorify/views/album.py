import json
import requests

from flask import Blueprint
from numpy import mean, median


albums = Blueprint("albums", __name__)

@albums.route("/<album_id>")
def get_track_data(album_id):
  url = "http://ws.spotify.com/lookup/1/.json" + \
          "?uri=spotify:album:%s&extras=trackdetail" % album_id
  resp = requests.get(url).json()
  artist = resp['album']['artist']
  album_name = resp['album']['name']
  tracks = resp['album']['tracks']

  pops = [float(t['popularity']) for t in tracks]
  pop_max = max(pops)
  pop_min = min(pops)
  pop_range = pop_max - pop_min
  pop_sum = sum(pops)

  rel_pop_sum = sum([(pop - pop_min) / pop_range for pop in pops])

  track_data = []
  last_track = 0
  current_disc = 1
  add_to_track = 0

  for t in tracks:
    pop = float(t['popularity'])
    rel_pop = (pop - pop_min) / pop_range
    share_pop = rel_pop / rel_pop_sum
    disc = int(t['disc-number'])
    track = int(t['track-number'])

    if disc > current_disc:
      current_disc = disc
      add_to_track += last_track

    track_data.append({
      'name':       t['name'],
      'num':        track + add_to_track,
      'pop':        pop,
      'rel_pop':    round(rel_pop, 3),
      'share_pop':  round(share_pop, 3)
    })

    last_track = track

  return json.dumps({
    'tracks': track_data,
    'max':    pop_max,
    'min':    pop_min,
    'mean':   mean(pops),
    'median': median(pops),
    'name':   album_name,
    'artist': artist,
  })
