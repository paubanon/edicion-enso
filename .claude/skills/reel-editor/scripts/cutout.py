"""Cut the person out of the reel's footage, for titles that sit behind them.

Usage: python3 cutout.py <reel-dir>    -> <reel>/public/cutout.webm

The cutout is the footage itself with the background made transparent (VP9 with
alpha), frame-aligned with public/main_cut.mp4, so a layer stack of
footage -> title -> cutout puts the title behind the person. Masks come from Apple
Vision person segmentation (scripts/person_mask.swift), compiled on first use.
"""
import json
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
SWIFT_SOURCE = SCRIPTS / "person_mask.swift"
BINARY = SCRIPTS / ".build" / "person_mask"
# Vision leaves faint alpha on background objects next to the body; this ramp drops
# alpha below MASK_FLOOR and saturates above MASK_CEIL, keeping a soft edge between.
MASK_FLOOR = 70
MASK_CEIL = 190
MASK_RAMP = f"lut=c0='clip((val-{MASK_FLOOR})*255/{MASK_CEIL - MASK_FLOOR},0,255)'"


def person_mask_binary():
    if not BINARY.exists() or BINARY.stat().st_mtime < SWIFT_SOURCE.stat().st_mtime:
        BINARY.parent.mkdir(exist_ok=True)
        subprocess.run(["swiftc", "-O", str(SWIFT_SOURCE), "-o", str(BINARY)], check=True)
    return BINARY


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,r_frame_rate", "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout
    stream = json.loads(out)["streams"][0]
    return stream["width"], stream["height"], Fraction(stream["r_frame_rate"])


def cut_out(video, out_path, encode_args):
    """Merge the footage with its person mask into a video or image with alpha."""
    width, height, fps = probe(video)
    mask = subprocess.Popen([str(person_mask_binary()), str(video), str(width), str(height)], stdout=subprocess.PIPE)
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(video),
         "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{width}x{height}", "-framerate", str(fps), "-i", "-",
         "-filter_complex", f"[1:v]format=gray,{MASK_RAMP}[m];[0:v][m]alphamerge[out]",
         "-map", "[out]", *encode_args, str(out_path)],
        stdin=mask.stdout, check=True,
    )
    if mask.wait() != 0:
        raise SystemExit("person_mask failed")


def cut_out_frame(video, out_path, seconds):
    """One frame as a 1080x1920 PNG with alpha, for the storyboard."""
    with tempfile.TemporaryDirectory() as tmp:
        # A one-frame clip, since the mask tool reads videos.
        still = Path(tmp) / "frame.mp4"
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-ss", f"{seconds:.3f}", "-i", str(video),
             "-frames:v", "1", "-an", "-vf", "scale=1080:1920", "-c:v", "libx264", "-crf", "12", str(still)],
            check=True,
        )
        cut_out(still, out_path, ["-frames:v", "1", "-pix_fmt", "rgba"])


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    reel = Path(sys.argv[1])
    out_path = reel / "public" / "cutout.webm"
    cut_out(
        reel / "public" / "main_cut.mp4", out_path,
        ["-an", "-pix_fmt", "yuva420p", "-c:v", "libvpx-vp9", "-b:v", "8M",
         "-deadline", "realtime", "-cpu-used", "8", "-row-mt", "1", "-auto-alt-ref", "0"],
    )
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
