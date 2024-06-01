import datetime as dt

import requests
from bs4 import BeautifulSoup

from .song_history import SongHistory
from .utils import Picture, Song, at_midnight


class LaRadioPlusSongHistory(SongHistory):
    """A class that can find a broadcasted song on La Radio Plus."""

    def fetch_song_history(self, date: dt.datetime):
        """Fill the `song_history` dict."""
        super().fetch_song_history(date)

        req = requests.get("https://alpesdusud.laradioplus.com/radio/history")
        soup = BeautifulSoup(req.text, "html.parser")

        song_elements = soup.select("div.row > div.col-12 > div")

        for song_element in song_elements:
            hour_el, picture_el, song_el, *_ = song_element.find_all("div", recursive=False)
            hour, _, minute = hour_el.text.partition(":")
            picture_url = picture_el.find("img").get("src")
            title, artist = song_el.text.strip().split("\n", 1)
            time = date.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0).timestamp()
            self.song_history[time] = Song(title=title, artists=[artist], picture=Picture(picture_url))

    @property
    def min_date(self):
        """The minimum date to find a song on La Radio Plus."""
        return at_midnight(self.now) - dt.timedelta(days=30)
