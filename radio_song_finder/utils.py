import datetime as dt
from dataclasses import dataclass, field


def at_midnight(datetime: dt.datetime):
    """Return the datetime that is equal to the passed date but at midnight."""
    return datetime.replace(hour=0, minute=0, second=0, microsecond=0)


@dataclass
class Picture:
    """A picture (album art) on a website."""

    CHUNK_SIZE = 64 * 1024

    url: str = ""
    width: int = 0
    height: int = 0

    def __repr__(self):
        return f"<Picture {self.width}x{self.height} at {self.url}>"


@dataclass
class Song:
    """A song."""

    title: str = ""
    artists: list[str] = field(default_factory=list)
    album: str | None = None
    duration: float = 0
    language: str | None = None
    genre: str | None = None
    composers: list[str] | None = field(default_factory=list)
    release_date: str | dt.date | None = None
    isrc: str | None = None
    track_number: int | tuple[int, int | None] | None = None
    copyright: str | None = None  # pylint: disable=W0622
    lyrics: str | list[tuple[str, float]] | None = None
    picture: Picture | str | None = None
    comments: str | None = None

    @classmethod
    def empty(cls):
        """Return an empty song for placeholder purposes."""
        return cls()

    def __not__(self):
        return not self.title and not self.artists

    def __repr__(self):
        return f"<Song '{self.title}' by {', '.join(self.artists)} album {self.album} {self.duration} s>"

    def __str__(self):
        return f"{', '.join(self.artists)} - {self.title}"
