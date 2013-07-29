import csv
import requests
import StringIO

from flask import Flask
app = Flask(__name__)


@app.route("/:album_id")
def get_track_data(album_id):
  resp = requests.get(
    "http:/ws.spotify.com/lookup/1/.json?uri=spotify:album:%s" % album_id)
  tracks = resp.json()['album']['tracks']
  track_data = [(t['name'], t['track-number'], t['popularity']) \
                for t in tracks]

  fp = StringIO.StringIO()
  writer = csv.writer(fp)
  track_data = sorted(track_data, key=lambda t: t[1])
  for track in track_data:
    name, num, pop = track
    writer.writerow([name, num, pop])

  writer.flush()
  return fp.getvalue()

if __name__ == "__main__":
  app.run()
