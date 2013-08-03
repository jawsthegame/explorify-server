import os

from spotify import AlbumBrowser
from spotify import Link
from spotify.manager.session import SpotifySessionManager


class ExplorifyManager(SpotifySessionManager):
  appkey_file = os.path.join(os.path.dirname(__file__), 'spotify_appkey.key')

  self._tracks = None

  def logged_in(self, session, error):
    def got_album(browser, error):
      tracks = []
      for track in browser:
        tracks.append({'num': track.index(), 'pop': track.popularity()})
      self._tracks = sorted(tracks, key=lambda t: t['num'])
      self.disconnect()

    link = Link.from_string("spotify:album:4DR0GWo7w2GJyQnFVa4jAB")
    album = link.as_album()

    browser = AlbumBrowser(album, got_album)

  def logged_out(session):
    pass
