"""Where a reel's material lives.

A reel called <Reel> has its takes in tomas/<Reel>/ (the user's, read-only) and
everything generated in ediciones/<Reel>/ (edit/, public/, src/, out/). Scripts take
the ediciones/<Reel> folder and find the takes from its name.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]


def takes_dir(reel: Path) -> Path:
    return REPO_ROOT / "tomas" / Path(reel).resolve().name
