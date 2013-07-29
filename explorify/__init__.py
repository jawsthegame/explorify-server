import json
import requests

from flask import Flask
from numpy import mean, median


app = Flask(__name__)

@app.route("/<album_id>")
def get_track_data(album_id):
  url = "http://ws.spotify.com/lookup/1/.json" + \
          "?uri=spotify:album:%s&extras=trackdetail" % album_id
  resp = requests.get(url)
  tracks = resp.json()['album']['tracks']

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
  })

if __name__ == "__main__":
  app.run()
