"""Check a rendered reel against the delivery spec and make small images to inspect.

Usage: python3 qa.py <video> [--at 1.2,5.8,...] [--tiles 24]

Prints PASS/FAIL per check (size, codec, pixel format, audio, loudness) and writes,
next to the video:
  <name>-sheet.jpg        contact sheet, one thumbnail every few seconds
  <name>-at-<t>.jpg       for each --at time, a half-size frame with Instagram's safe
                          zone outlined, to check faces, cropping and legibility
Images are kept small on purpose: they are read by the model, and pixels cost tokens.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

SPEC = {"width": 1080, "height": 1920, "codec_name": "h264", "pix_fmt": "yuv420p"}
TARGET_LUFS = -14
LUFS_TOLERANCE = 2
SAFE = {"top": 220, "bottom": 420, "left": 60, "right": 140}
THUMB_WIDTH = 180
COLUMNS = 8


def probe(video):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_type,codec_name,width,height,pix_fmt,r_frame_rate:format=duration", "-of", "json", str(video)],
        check=True, capture_output=True, text=True,
    ).stdout
    info = json.loads(out)
    video_stream = next(s for s in info["streams"] if s["codec_type"] == "video")
    has_audio = any(s["codec_type"] == "audio" for s in info["streams"])
    return video_stream, has_audio, float(info["format"]["duration"])


def integrated_loudness(video):
    log = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(video), "-vn", "-af", "ebur128", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    match = re.findall(r"I:\s+(-?[\d.]+) LUFS", log)
    return float(match[-1]) if match else None


def contact_sheet(video, duration, tiles, out_path):
    step = max(duration / tiles, 0.5)
    rows = -(-int(duration / step + 1) // COLUMNS)
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vf",
         f"fps=1/{step:.3f},scale={THUMB_WIDTH}:-2,tile={COLUMNS}x{rows}:padding=3",
         "-frames:v", "1", str(out_path)],
        check=True,
    )
    return step


def frame_with_safe_zone(video, seconds, out_path):
    box = f"drawbox=x={SAFE['left']}:y={SAFE['top']}:w=iw-{SAFE['left'] + SAFE['right']}:h=ih-{SAFE['top'] + SAFE['bottom']}:color=red@0.8:t=4"
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-ss", f"{seconds:.3f}", "-i", str(video),
         "-frames:v", "1", "-vf", f"{box},scale=540:-2", "-q:v", "4", str(out_path)],
        check=True,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("--at", default="", help="comma-separated seconds to export with the safe zone")
    parser.add_argument("--tiles", type=int, default=24)
    args = parser.parse_args()

    stream, has_audio, duration = probe(args.video)
    checks = [(f"{key}={stream.get(key)}", stream.get(key) == want) for key, want in SPEC.items()]
    checks.append(("audio track", has_audio))
    if has_audio:
        lufs = integrated_loudness(args.video)
        checks.append((f"loudness {lufs} LUFS (target {TARGET_LUFS})", lufs is not None and abs(lufs - TARGET_LUFS) <= LUFS_TOLERANCE))
    for label, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {label}")
    print(f"      duration {duration:.2f}s, fps {stream.get('r_frame_rate')}")

    stem = args.video.with_suffix("")
    sheet = Path(f"{stem}-sheet.jpg")
    step = contact_sheet(args.video, duration, args.tiles, sheet)
    # Unlabelled (Homebrew's ffmpeg has no drawtext): tile n shows second n * step.
    print(f"sheet {sheet} (one tile every {step:.2f}s, left to right, top to bottom)")
    for t in filter(None, args.at.split(",")):
        out = Path(f"{stem}-at-{float(t):.2f}.jpg")
        frame_with_safe_zone(args.video, float(t), out)
        print(f"frame {out}")


if __name__ == "__main__":
    main()
