import json
import requests

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

  track_data = []
  for t in tracks:
    pop = float(t['popularity'])
    track_data.append({
      'name':     t['name'],
      'num':      int(t['track-number']),
      'pop':      pop,
      'rel_pop':  round((pop - pop_min) / pop_range, 2)
    })

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
  if origin in ['null', 'http://explorify.tomfleischer.com']:
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = \
      'Content-Type, Pragma, Cache-Control, *'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
  return response


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5001)
