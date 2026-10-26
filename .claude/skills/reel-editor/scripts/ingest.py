"""Probe, preview and transcribe the raw takes of a reel.

Usage: python3 ingest.py ediciones/<Reel> [--vocab "EnsoMovers, pancake, ..."] [--force]

Transcription uses the `mlx_whisper` command (installed with `uv tool install mlx-whisper`).

Reads   tomas/<Reel>/*.(mp4|mov)   (see paths.py)
Writes  <reel>/edit/clips.md        one row per take: role, duration, fps, size, note
        <reel>/edit/overview.jpg    one thumbnail per take, in clips.md order
        <reel>/edit/words/<take>.json   word timings (source seconds)
        <reel>/edit/transcript.md   compact phrase-level transcript to read instead of the JSON

Take names follow the user's convention: the leading number is the script line
(`6.1`, `6.2` are parts of line 6), `<n>_<letter>_<desc>` is B-roll for line n, and
any other text after the number is a note (`11_pendiente_ilustrar`). B-roll is not
transcribed. Takes that already have a words file are skipped unless --force is given,
so it is safe to re-run after adding takes.
"""
import argparse
import json
import re
import subprocess
import tempfile
from fractions import Fraction
from pathlib import Path

from paths import takes_dir as find_takes_dir

MODEL = "mlx-community/whisper-large-v3-turbo"
LANGUAGE = "es"
VIDEO_SUFFIXES = {".mp4", ".mov"}
THUMB_WIDTH = 180
THUMB_HEIGHT = 320
SHEET_COLUMNS = 8
TAKE_NAME = re.compile(r"^(?P<line>\d+(?:\.\d+)?)(?:_(?P<broll>[a-z])_(?P<desc>.+)|_(?P<note>.+))?$")
# Whisper's word boundaries drift; a gap this long starts a new transcript line.
LINE_BREAK_GAP = 0.6


def parse_take(path):
    """Script line, role and note encoded in a take's file name."""
    match = TAKE_NAME.match(path.stem)
    if not match:
        return {"line": (float("inf"),), "role": "?", "note": path.stem}
    line = tuple(int(n) for n in match["line"].split("."))
    if match["broll"]:
        return {"line": line, "role": f"B-roll {match['broll']}", "note": match["desc"].replace("_", " ")}
    return {"line": line, "role": "voz", "note": (match["note"] or "").replace("_", " ")}


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,r_frame_rate:stream_side_data=rotation:format=duration",
         "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout
    info = json.loads(out)
    stream = info["streams"][0]
    rotation = abs(int(next((s.get("rotation", 0) for s in stream.get("side_data_list", [])), 0)))
    width, height = stream["width"], stream["height"]
    if rotation in (90, 270):
        width, height = height, width
    return {
        "duration": float(info["format"]["duration"]),
        "fps": float(Fraction(stream["r_frame_rate"])),
        "width": width,
        "height": height,
    }


def write_overview(takes, infos, out_path):
    """One mid-take thumbnail per take, tiled left to right in the order of clips.md.

    Unlabelled: Homebrew's ffmpeg is built without drawtext.
    """
    inputs, filters = [], []
    for i, (take, info) in enumerate(zip(takes, infos)):
        inputs += ["-ss", f"{info['duration'] / 2:.2f}", "-i", str(take)]
        # A fixed box per thumbnail, so vertical and horizontal takes tile together.
        filters.append(
            f"[{i}:v]trim=end_frame=1,scale={THUMB_WIDTH}:{THUMB_HEIGHT}:force_original_aspect_ratio=decrease,"
            f"pad={THUMB_WIDTH}:{THUMB_HEIGHT}:(ow-iw)/2:(oh-ih)/2,setsar=1[t{i}]"
        )
    rows = -(-len(takes) // SHEET_COLUMNS)
    labels = "".join(f"[t{i}]" for i in range(len(takes)))
    filters.append(f"{labels}concat=n={len(takes)}:v=1,tile={SHEET_COLUMNS}x{rows}:padding=3[sheet]")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filters),
         "-map", "[sheet]", "-frames:v", "1", str(out_path)],
        check=True,
    )


def transcribe(take, vocab):
    with tempfile.TemporaryDirectory() as tmp:
        command = [
            "mlx_whisper", str(take), "--model", MODEL, "--language", LANGUAGE,
            "--word-timestamps", "True", "--condition-on-previous-text", "False",
            "--output-format", "json", "--output-dir", tmp, "--output-name", "words", "--verbose", "False",
        ]
        if vocab:
            command += ["--initial-prompt", vocab]
        # Quiet unless it fails: progress bars only cost tokens when read back.
        run = subprocess.run(command, capture_output=True, text=True)
        if run.returncode != 0:
            raise SystemExit(f"mlx_whisper failed on {take.name}:\n{run.stderr[-2000:]}")
        result = json.loads((Path(tmp) / "words.json").read_text())
    return [
        {"word": w["word"].strip(), "start": round(w["start"], 3), "end": round(w["end"], 3)}
        for segment in result["segments"]
        for w in segment.get("words", [])
        if w["word"].strip()
    ]


def transcript_lines(words):
    lines, current = [], []
    for word in words:
        if current and word["start"] - current[-1]["end"] > LINE_BREAK_GAP:
            lines.append(current)
            current = []
        current.append(word)
    if current:
        lines.append(current)
    return [f"[{line[0]['start']:.2f}–{line[-1]['end']:.2f}] {' '.join(w['word'] for w in line)}" for line in lines]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("reel", type=Path)
    parser.add_argument("--vocab", default="", help="names and jargon to bias the spelling")
    parser.add_argument("--force", action="store_true", help="re-transcribe takes that already have words")
    args = parser.parse_args()

    takes_dir = find_takes_dir(args.reel)
    edit = args.reel / "edit"
    words_dir = edit / "words"
    words_dir.mkdir(parents=True, exist_ok=True)

    takes = [p for p in takes_dir.iterdir() if p.suffix.lower() in VIDEO_SUFFIXES and not p.name.startswith(".")]
    if not takes:
        raise SystemExit(f"no takes in {takes_dir}")
    names = {t: parse_take(t) for t in takes}
    takes.sort(key=lambda t: (names[t]["line"], names[t]["role"] != "voz", t.name))
    infos = [probe(t) for t in takes]

    rows = ["| take | papel | s | fps | size | nota |", "|---|---|---|---|---|---|"]
    rows += [
        f"| {t.name} | {names[t]['role']} | {i['duration']:.1f} | {i['fps']:g} | {i['width']}x{i['height']} | {names[t]['note']} |"
        for t, i in zip(takes, infos)
    ]
    (edit / "clips.md").write_text("\n".join(rows) + "\n")
    write_overview(takes, infos, edit / "overview.jpg")

    transcript = []
    for take in takes:
        if names[take]["role"].startswith("B-roll"):
            continue
        words_path = words_dir / f"{take.stem}.json"
        if args.force or not words_path.exists():
            print(f"transcribing {take.name}", flush=True)
            words_path.write_text(json.dumps(transcribe(take, args.vocab), ensure_ascii=False, indent=0))
        words = json.loads(words_path.read_text())
        transcript.append(f"## {take.name}\n" + ("\n".join(transcript_lines(words)) or "(sin voz)"))
    (edit / "transcript.md").write_text("\n\n".join(transcript) + "\n")

    fps_set = {i["fps"] for i in infos}
    print(f"{len(takes)} takes, {sum(i['duration'] for i in infos):.0f}s total, fps {sorted(fps_set)}")
    print(f"wrote {edit / 'clips.md'}, {edit / 'overview.jpg'}, {edit / 'transcript.md'}")


if __name__ == "__main__":
    main()
