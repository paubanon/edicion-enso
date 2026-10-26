# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy"]
# ///
"""Cut the chosen takes into the reel's spoken track and export the edit timeline.

Usage: uv run cut.py <reel-dir>

Reads   <reel>/edit/cut.json          which takes (and source ranges) to keep, in order
        <reel>/edit/words/<take>.json word timings from ingest.py
Writes  <reel>/public/main_cut.mp4    tightened footage + processed voice
        <reel>/src/edit.json          fps, size, shots and captions on the output timeline
        <reel>/edit/cut_transcript.md what is said at which output frame, for placing cues

cut.json:
  {
    "fps": 25,                      optional, defaults to the first take's frame rate
    "size": [1440, 2560],           optional, footage size; larger than 1080x1920 keeps punch-ins sharp
    "voice": ["highpass=f=80", …],  optional ffmpeg audio chain replacing VOICE_CHAIN
    "keep": [
      {"take": "1.mp4"},                      whole take
      {"take": "6.2.mp4", "from": 2.1, "to": 7.4, "note": "frase"},
      {"take": "7.mp4", "tighten": false}         keep pauses, only when the user asks for a silence
    ]
  }

Range boundaries are refined against the audio energy and pauses longer than MIN_PAUSE
are tightened (unless "tighten" is false), so ranges only need to be rough. Dialogue
runs continuously, also through demonstrations (he demonstrates while he talks).
Breathing or moving close to the mic can still pass for speech: split the range to
drop it.
"""
import json
import subprocess
import sys
import tempfile
import wave
from fractions import Fraction
from pathlib import Path

import numpy as np

AUDIO_RATE = 48000
ENERGY_HOP = 0.01

MIN_PAUSE = 0.2  # pauses longer than this get tightened
LEAD_IN = 0.07  # silence kept before speech resumes
LEAD_OUT = 0.1  # silence kept after speech stops
SNAP_WINDOW = 0.08  # mid-speech boundaries snap to the quietest 10 ms within this window
MIN_BLIP = 0.05  # louder-than-threshold runs shorter than this are noise, not speech
VOICE_RANGE = 25  # dB below the take's typical voice level still counted as speech; breaths and movement sit lower
WORD_TAIL = 0.2  # end of each transcribed word counted as speech, for words too quiet to detect
TAIL_REACH = 0.15  # ...only when detected speech lies this close to the word
EDGE_FADE = 0.006  # per-piece audio fade, removes clicks at cut points
SHOT_BREAK = 0.6  # removing at least this much source time starts a new camera "shot"
OUTPUT_SIZE = (1080, 1920)  # composition size; the footage may be larger

VOICE_CHAIN = [
    "highpass=f=80",
    "acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80:makeup=2",
    "loudnorm=I=-14:TP=-1.5:LRA=9",
]


def probe_fps(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
         "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout
    return float(Fraction(json.loads(out)["streams"][0]["r_frame_rate"]))


def load_audio(path):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "2",
         "-ar", str(AUDIO_RATE), "-f", "f32le", "-"],
        check=True, capture_output=True,
    ).stdout
    return np.frombuffer(raw, dtype="<f4").reshape(-1, 2)


def energy_db(audio):
    mono = audio.mean(axis=1)
    hop = int(AUDIO_RATE * ENERGY_HOP)
    frames = len(mono) // hop
    power = (mono[: frames * hop].reshape(frames, hop) ** 2).mean(axis=1)
    return 10 * np.log10(power + 1e-12)


def speech_mask(db):
    # Above the noise floor is not enough in a quiet room: breathing and moving on the
    # floor clear it too, so speech must also be within VOICE_RANGE of the voice.
    floor = np.percentile(db, 20) + 8
    voice = np.median(db[db > floor])
    loud = db > max(floor, voice - VOICE_RANGE)
    # Drop clicks too short to be speech.
    min_run = int(MIN_BLIP / ENERGY_HOP)
    i = 0
    while i < len(loud):
        if loud[i]:
            j = i
            while j < len(loud) and loud[j]:
                j += 1
            if j - i < min_run:
                loud[i:j] = False
            i = j
        else:
            i += 1
    return loud


def with_word_tails(speech, words):
    """Mark the end of quiet transcribed words as speech.

    Quiet words ("y", "si") fall under the energy threshold and would be cut. Whisper's
    word starts drift early into silence, but its ends are close, so only each word's
    last WORD_TAIL seconds count. Words with detected speech of their own need no tail,
    and a word with no detected speech within TAIL_REACH is Whisper stretching into a
    pause: a tail there would keep the pause.
    """
    marked = speech.copy()
    reach = int(TAIL_REACH / ENERGY_HOP)
    for word in words:
        start, end = int(word["start"] / ENERGY_HOP), int(word["end"] / ENERGY_HOP) + 1
        if speech[start:end].any() or not speech[max(0, start - reach): end + reach].any():
            continue
        lo = int(max(word["start"], word["end"] - WORD_TAIL) / ENERGY_HOP)
        marked[lo:end] = True
    return marked


def snap_to_quietest(t, db):
    lo = max(0, int((t - SNAP_WINDOW) / ENERGY_HOP))
    hi = int((t + SNAP_WINDOW) / ENERGY_HOP) + 1
    return (lo + int(np.argmin(db[lo:hi]))) * ENERGY_HOP


def speech_runs(start, end, speech):
    """Speech runs within [start, end], bridging pauses shorter than MIN_PAUSE."""
    lo, hi = int(start / ENERGY_HOP), min(int(end / ENERGY_HOP), len(speech))
    runs = []
    i = lo
    while i < hi:
        if not speech[i]:
            i += 1
            continue
        j = i
        while j < hi and speech[j]:
            j += 1
        if runs and (i - runs[-1][1]) * ENERGY_HOP < MIN_PAUSE:
            runs[-1][1] = j
        else:
            runs.append([i, j])
        i = j
    return [(a * ENERGY_HOP, b * ENERGY_HOP) for a, b in runs]


def build_pieces(keep, takes, fps):
    """Kept speech as frame ranges of their takes, laid end to end on the output timeline."""
    pieces = []
    for entry in keep:
        take = takes[entry["take"]]
        db, speech = take["db"], take["speech"]
        start = entry.get("from", 0.0)
        end = entry.get("to", len(db) * ENERGY_HOP)
        if speech[min(int(start / ENERGY_HOP), len(speech) - 1)]:
            start = snap_to_quietest(start, db)
        if speech[min(int(end / ENERGY_HOP), len(speech) - 1)]:
            end = snap_to_quietest(end, db)
        runs = speech_runs(start, end, speech) if entry.get("tighten", True) else [(start + LEAD_IN, end - LEAD_OUT)]
        for run_start, run_end in runs:
            src_from = round(max(start, run_start - LEAD_IN) * fps)
            src_to = round(min(end, run_end + LEAD_OUT) * fps)
            last = pieces[-1] if pieces else None
            if last and last["take"] == entry["take"] and src_from <= last["srcTo"]:
                last["srcTo"] = max(last["srcTo"], src_to)
            elif src_to > src_from:
                pieces.append({"take": entry["take"], "srcFrom": src_from, "srcTo": src_to})
    out = 0
    for piece in pieces:
        piece["from"] = out
        out += piece["srcTo"] - piece["srcFrom"]
    return pieces, out


def build_shots(pieces, fps):
    shots = [{"from": 0, "take": pieces[0]["take"]}]
    for previous, piece in zip(pieces, pieces[1:]):
        if piece["take"] != previous["take"] or (piece["srcFrom"] - previous["srcTo"]) / fps >= SHOT_BREAK:
            shots.append({"from": piece["from"], "take": piece["take"]})
    return shots


def place_words(pieces, words_by_take, fps):
    """Words on the output timeline, each in the first kept piece it overlaps.

    Whisper's word bounds swallow neighbouring silence, so a word may start before
    its piece; it is clamped to the piece instead of dropped.
    """
    placed = []
    for take, words in words_by_take.items():
        take_pieces = [p for p in pieces if p["take"] == take]
        for word in words:
            piece = next((p for p in take_pieces if word["start"] < p["srcTo"] / fps and word["end"] > p["srcFrom"] / fps), None)
            if piece is None:
                continue
            lo, length = piece["srcFrom"] / fps, piece["srcTo"] - piece["srcFrom"]
            start = piece["from"] + max(0, round((word["start"] - lo) * fps))
            end = max(start + 1, piece["from"] + min(round((word["end"] - lo) * fps), length))
            placed.append({"word": word["word"], "from": start, "to": end})
    return sorted(placed, key=lambda w: w["from"])


def voiced_cuts(pieces, takes, fps):
    """Piece edges that land on speech, where a syllable may be clipped."""
    found = []
    for piece in pieces:
        speech = takes[piece["take"]]["speech"]
        for edge in (piece["srcFrom"], piece["srcTo"]):
            if speech[min(int(edge / fps / ENERGY_HOP), len(speech) - 1)]:
                found.append(f"{piece['take']} {edge / fps:.2f}s (salida f{piece['from'] + edge - piece['srcFrom']})")
    return found


def to_captions(placed, fps):
    return [
        {
            "text": " " + w["word"],
            "startMs": round(w["from"] / fps * 1000),
            "endMs": round(w["to"] / fps * 1000),
            "timestampMs": None,
            "confidence": None,
        }
        for w in placed
    ]


def write_cut_transcript(path, placed, shots, fps):
    shot_starts = {s["from"]: s["take"] for s in shots}
    lines, current = [], []

    def flush():
        if current:
            a, b = current[0]["from"], current[-1]["to"]
            lines.append(f"f{a:>5}–{b:<5} {a / fps:6.2f}s  " + " ".join(w["word"] for w in current))
        current.clear()

    for word in placed:
        starts_shot = any(current and current[-1]["to"] <= s <= word["from"] for s in shot_starts)
        if current and (starts_shot or word["from"] - current[-1]["to"] > fps // 2 or current[-1]["word"][-1:] in ".?!"):
            flush()
        current.append(word)
    flush()
    header = f"# Corte · {fps:g} fps · plano nuevo en: " + ", ".join(f"f{f} ({t})" for f, t in shot_starts.items())
    path.write_text(header + "\n\n" + "\n".join(lines) + "\n")


def render(pieces, takes, fps, size, voice_chain, out_path):
    samples_per_frame = AUDIO_RATE / fps
    fade = int(EDGE_FADE * AUDIO_RATE)
    ramp = (0.5 - 0.5 * np.cos(np.linspace(0, np.pi, fade)))[:, None]
    chunks = []
    for piece in pieces:
        audio = takes[piece["take"]]["audio"]
        n = round((piece["srcTo"] - piece["srcFrom"]) * samples_per_frame)
        start = round(piece["srcFrom"] * samples_per_frame)
        chunk = np.zeros((n, 2), dtype=np.float32)
        available = audio[start: start + n]
        chunk[: len(available)] = available
        chunk[:fade] *= ramp
        chunk[-fade:] *= ramp[::-1]
        chunks.append(chunk)
    voice = np.concatenate(chunks)

    width, height = size
    video_filter = (
        f"fps={fps},scale={width}:{height}:force_original_aspect_ratio=increase:flags=lanczos,"
        f"crop={width}:{height},setsar=1"
    )
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        listing = []
        for i, piece in enumerate(pieces):
            part = tmp / f"part{i:03}.mp4"
            subprocess.run(
                ["ffmpeg", "-v", "error", "-y", "-ss", f"{piece['srcFrom'] / fps:.4f}",
                 "-i", str(takes[piece["take"]]["path"]),
                 "-vf", video_filter, "-frames:v", str(piece["srcTo"] - piece["srcFrom"]), "-an",
                 "-c:v", "h264_videotoolbox", "-b:v", "40M", "-g", str(round(fps / 2)),
                 "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                 str(part)],
                check=True,
            )
            listing.append(f"file '{part}'")
        (tmp / "parts.txt").write_text("\n".join(listing))

        voice_path = tmp / "voice.wav"
        with wave.open(str(voice_path), "wb") as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(AUDIO_RATE)
            wav.writeframes((np.clip(voice, -1, 1) * 32767).astype("<i2").tobytes())

        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(tmp / "parts.txt"),
             "-i", str(voice_path), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
             "-af", ",".join(voice_chain), "-c:a", "aac", "-b:a", "256k", "-ar", str(AUDIO_RATE),
             "-movflags", "+faststart", str(out_path)],
            check=True,
        )


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    reel = Path(sys.argv[1])
    spec = json.loads((reel / "edit" / "cut.json").read_text())

    names = list(dict.fromkeys(entry["take"] for entry in spec["keep"]))
    words_by_take = {n: json.loads((reel / "edit" / "words" / f"{Path(n).stem}.json").read_text()) for n in names}
    takes = {}
    for name in names:
        path = reel / "tomas" / name
        audio = load_audio(path)
        db = energy_db(audio)
        takes[name] = {"path": path, "audio": audio, "db": db, "speech": with_word_tails(speech_mask(db), words_by_take[name])}
    fps = spec.get("fps") or probe_fps(takes[names[0]]["path"])
    mismatched = [n for n in names if abs(probe_fps(takes[n]["path"]) - fps) > 0.01]
    if mismatched:
        print(f"aviso: {', '.join(mismatched)} no van a {fps:g} fps; se convierten", file=sys.stderr)

    pieces, duration = build_pieces(spec["keep"], takes, fps)
    placed = place_words(pieces, words_by_take, fps)
    clipped = voiced_cuts(pieces, takes, fps)
    shots = build_shots(pieces, fps)

    (reel / "public").mkdir(exist_ok=True)
    (reel / "src").mkdir(exist_ok=True)
    edit = {
        "fps": fps,
        "width": OUTPUT_SIZE[0],
        "height": OUTPUT_SIZE[1],
        "durationInFrames": duration,
        "shots": shots,
        "captions": to_captions(placed, fps),
    }
    (reel / "src" / "edit.json").write_text(json.dumps(edit, ensure_ascii=False, indent=1))
    write_cut_transcript(reel / "edit" / "cut_transcript.md", placed, shots, fps)
    render(pieces, takes, fps, tuple(spec.get("size", (1440, 2560))), spec.get("voice", VOICE_CHAIN),
           reel / "public" / "main_cut.mp4")

    print(f"{len(pieces)} pieces, {len(shots)} shots, {duration / fps:.1f}s output at {fps:g} fps")
    for line in clipped:
        print(f"aviso: corte sobre voz, puede comerse una sílaba: {line}")


if __name__ == "__main__":
    main()
