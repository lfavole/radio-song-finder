from pathlib import Path

from PyInstaller.__main__ import run

BASE_PATH = Path(__file__).parent

exclusions = [
    "statistics",  # imported by random
]
exclusions_args = []
for excl in exclusions:
    exclusions_args.append("--exclude-module")
    exclusions_args.append(excl)

run(
    [
        "--onefile",
        "--name",
        "radio-song-finder",
        *exclusions_args,
        str(BASE_PATH / "radio_song_finder/__main__.py"),
    ]
)
