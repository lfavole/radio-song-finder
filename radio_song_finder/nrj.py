import datetime as dt

import requests

from .song_history import SongHistory
from .utils import Song, at_midnight


class NRJSongHistory(SongHistory):
    """A class that can find a broadcasted song on NRJ."""

    def __init__(self):
        super().__init__()
        self._fetched_yesterday = False
        self._fetched_today = False

    def fetch_song_history(self, date):
        """Fill the `song_history` dict."""
        yesterday = date < at_midnight(self.now)
        if yesterday and self._fetched_yesterday:
            return
        if not yesterday and self._fetched_today:
            return

        req = requests.get("https://www.nrj.fr/chansons-diffusees.json" + ("?yesterday=1" if yesterday else ""))
        data = req.json()
        for song in data.get("songs", {}).values():
            time = song.get("time")
            if time is None:
                continue
            self.song_history[time] = Song(title=song.get("title", ""), artists=[song.get("artist", "")])
            # TODO duration ? + picture

    @property
    def min_date(self):
        """The minimum date to find a song on NRJ."""
        return at_midnight(self.now) - dt.timedelta(days=1)
