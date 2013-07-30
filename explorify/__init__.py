import json
import requests

from collections import defaultdict
from flask import Flask
from numpy import mean, median


app = Flask(__name__)

@app.route("/<album_id>")
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
      'rel_pop':    round(rel_pop, 2),
      'share_pop':  round(share_pop, 2)
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

@app.after_request
def add_cors_header(response):
  from flask import request
  origin = request.headers.get('Origin', '')
  if origin in ['http://localhost:9000', 'http://explorify.jawsapps.com']:
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = \
      'Content-Type, Pragma, Cache-Control, *'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
  return response


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5001)
