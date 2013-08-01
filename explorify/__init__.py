from flask import Flask

from explorify.views.album import albums
from explorify.views.artist import artists


app = Flask(__name__)
app.register_blueprint(albums, url_prefix='/album')
app.register_blueprint(artists, url_prefix='/artist')

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
