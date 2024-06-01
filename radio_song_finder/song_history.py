import datetime as dt

from .utils import Song


class SongHistory:
    """A class that can find a broadcasted song on a radio."""

    def __init__(self):
        self.now = dt.datetime.now()
        self.song_history: dict[float, Song] = {}

    def fetch_song_history(self, date: dt.datetime):
        """Fill the `song_history` dict."""
        if date < self.min_date:
            raise ValueError(f"Can't get the song that was broadcasted at {date} because it's too far")

    @property
    def min_date(self) -> dt.datetime:
        """The minimum date to find a song on the radio."""
        raise NotImplementedError

    def get_song_at_time(self, date: dt.datetime):
        """Return the song that was broadcasted on a specific time."""
        self.fetch_song_history(date)
        target_timestamp = date.timestamp()

        ret = None
        for timestamp, song in self.song_history.items():
            if timestamp <= target_timestamp:
                ret = song
        return ret
