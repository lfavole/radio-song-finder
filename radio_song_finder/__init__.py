"""
Radio song finder.
"""

import argparse
import datetime as dt
import logging
import re
import sys
from typing import Type

from .laradioplus import LaRadioPlusSongHistory
from .nrj import NRJSongHistory
from .song_history import SongHistory

FINDERS: dict[str, Type[SongHistory]] = {
    "laradioplus": LaRadioPlusSongHistory,
    "nrj": NRJSongHistory,
}

__version__ = "2024.5.22"

logger = logging.getLogger(__name__)

# add a newline between each message on Termux
logging.basicConfig(format="[%(name)s] %(message)s" + ("\n" if hasattr(sys, "getandroidapilevel") else ""))


def find_song_on_radio(radio: str, time: str | dt.datetime | dt.time):
    """
    Find a song on a radio.
    """

    logger.debug("Parsing time: %s", time)

    if isinstance(time, str):
        match = re.match(r"^(\d+):(\d+)(?::(\d+))?$", time)
        if match:
            time = dt.time(int(match[1]), int(match[2]), int(match[3] or 0))
        else:
            time = dt.datetime.fromisoformat(time)

    if isinstance(time, dt.time):
        time = dt.datetime.combine(dt.date.today(), time)

    logger.info("Finding the song that was broadcasted at %s on %s", time, radio)
    finder = FINDERS[radio]
    song = finder().get_song_at_time(time)

    if song:
        logger.info("Found song!")
    else:
        logger.info("Sorry, no song found")
    return time, song


def main():
    """
    Main entry point for CLI.
    """
    parser = argparse.ArgumentParser(fromfile_prefix_chars="@")
    parser.add_argument("TIME", nargs="+", help="hours where to find the songs")
    parser.add_argument("--radio", help="radio where to find the songs")
    parser.add_argument("-v", "--verbose", action="count", help="show more information")

    args = parser.parse_args()

    logging.root.setLevel(
        {
            0: logging.WARNING,
            1: logging.INFO,
            2: logging.DEBUG,
        }.get(args.verbose, logging.DEBUG)
    )

    ret = []

    for time in args.TIME:
        time, song = find_song_on_radio(args.radio, time)
        ret.append((time, song))
        if song:
            print(f"{time}: {song}")

    return ret


if __name__ == "__main__":
    main()
