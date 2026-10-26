"""Build the storyboard page for a reel: one real frame per beat with its design on top.

Usage: python3 storyboard.py <reel-dir> [--open]

Reads   <reel>/edit/storyboard.json   beats, written by Claude (format in STORYBOARD.md)
        <reel>/public/main_cut.mp4    the cut, from cut.py
Writes  <reel>/edit/storyboard.html   the page to review
        <reel>/edit/storyboard/       frames and person cut-outs it shows

Overlays are HTML in composition pixels (1080x1920), the same coordinates and type
styles the Remotion build uses, so an approved frame translates directly. Frames and
cut-outs are cached; delete edit/storyboard/ to refresh them after a re-cut.
"""
import argparse
import html
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cutout import cut_out_frame  # noqa: E402

PREVIEW_SCALE = 1 / 3
PAGE = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · storyboard</title>
<style>
@font-face {{ font-family: Satoshi; src: url("../public/marca/fuentes/Satoshi-Variable.ttf"); font-weight: 300 900; }}
@font-face {{ font-family: Satoshi; src: url("../public/marca/fuentes/Satoshi-VariableItalic.ttf"); font-weight: 300 900; font-style: italic; }}
@font-face {{ font-family: "Fira Sans"; src: url("../public/marca/fuentes/FiraSans-Light.ttf"); font-weight: 300; }}
@font-face {{ font-family: "Fira Sans"; src: url("../public/marca/fuentes/FiraSans-LightItalic.ttf"); font-weight: 300; font-style: italic; }}
@font-face {{ font-family: "Fira Sans"; src: url("../public/marca/fuentes/FiraSans-Bold.ttf"); font-weight: 700; }}
@font-face {{ font-family: "JetBrains Mono"; src: url("../public/marca/fuentes/JetBrainsMono-Variable.ttf"); font-weight: 100 800; }}
/* Luminous Enso Pure, same tokens as lib/theme.ts */
:root {{ --black: #0A0A0A; --white: #FFFFFF; --mist: #E5E8E4; --card: #F8F9F7; --sage: #A2B598; --sage-light: #D4DECE; --earth: #8C7565; --scale: {scale}; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; padding: 32px 24px 64px; background: var(--black); color: var(--mist); font: 15px/1.45 "Fira Sans", system-ui, sans-serif; font-weight: 300; }}
header {{ max-width: 1400px; margin: 0 auto 28px; }}
h1 {{ font-size: 28px; margin: 0 0 6px; }}
header p {{ margin: 0; color: #9a9a9a; max-width: 70ch; }}
label {{ display: inline-flex; gap: 6px; margin-top: 12px; color: #9a9a9a; cursor: pointer; }}
.grid {{ max-width: 1400px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 36px 24px; }}
.beat {{ display: flex; flex-direction: column; gap: 10px; }}
.screen {{ width: calc(1080px * var(--scale)); height: calc(1920px * var(--scale)); position: relative; overflow: hidden; border-radius: 10px; background: #000; }}
.stage {{ width: 1080px; height: 1920px; position: absolute; inset: 0; transform: scale(var(--scale)); transform-origin: 0 0; }}
.stage > img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; filter: var(--grade); }}
.layer {{ position: absolute; inset: 0; }}
.safe {{ display: none; position: absolute; inset: 220px 140px 420px 60px; outline: 4px dashed rgba(255,80,80,.9); }}
body.show-safe .safe {{ display: block; }}
.meta {{ width: calc(1080px * var(--scale)); }}
.meta .time {{ color: #9a9a9a; font-variant-numeric: tabular-nums; }}
.meta .said {{ margin: 4px 0; font-style: italic; }}
.meta .notes {{ color: #bdbdbd; white-space: pre-line; }}
/* Type styles shared with lib/BigTitle, lib/Captions and lib/theme.ts.
   Over footage: white, key word in sage, wide shadow. On cards and paper: black,
   key word on a sage marker. */
.layer, .caption {{ --text: var(--white); --accent: var(--sage); --shadow: 0 3px 10px rgba(10,10,10,.45), 0 10px 60px rgba(10,10,10,.4); }}
.card, .paper {{ --text: var(--black); --accent: var(--black); --shadow: none; }}
.display {{ font-family: Satoshi, sans-serif; font-weight: 700; text-transform: uppercase; letter-spacing: -0.01em; line-height: .95; color: var(--text); text-shadow: var(--shadow); }}
.contrast {{ font-family: "Fira Sans", sans-serif; font-weight: 300; font-style: italic; letter-spacing: -0.02em; line-height: .95; color: var(--accent); text-shadow: var(--shadow); }}
.data {{ font-family: "JetBrains Mono", monospace; letter-spacing: -0.02em; color: var(--accent); text-shadow: var(--shadow); }}
.caption {{ position: absolute; left: 90px; right: 90px; top: 1260px; text-align: center; font-family: "Fira Sans", sans-serif; font-weight: 700; font-size: 60px; line-height: 1.15; color: var(--text); text-shadow: var(--shadow); }}
.caption b {{ color: var(--accent); font-weight: 700; }}
.mark {{ color: var(--accent); }}
.card .mark, .paper .mark {{ background: linear-gradient(transparent 58%, var(--sage) 58%, var(--sage) 92%, transparent 92%); }}
/* Card: the standard label (mono meta line + Satoshi title), white over bright footage. */
.card {{ position: absolute; background: var(--card); color: var(--black); border-radius: 26px; padding: 28px 34px; box-shadow: 0 24px 60px rgba(10,10,10,.28), 0 4px 12px rgba(10,10,10,.12); font-family: "Fira Sans", sans-serif; font-weight: 300; }}
.card strong {{ font-weight: 700; }}
.card .meta {{ font-family: "JetBrains Mono", monospace; font-size: 26px; color: var(--earth); letter-spacing: 0; }}
.card .title {{ font-family: Satoshi, sans-serif; font-weight: 700; text-transform: uppercase; font-size: 50px; line-height: 1; margin-top: 10px; }}
.card .row {{ display: flex; align-items: center; gap: 22px; }}
.badge {{ flex: none; width: 64px; height: 64px; border-radius: 50%; display: grid; place-items: center; font: 700 38px Satoshi, sans-serif; color: var(--white); }}
.badge.yes {{ background: var(--sage); }}
.badge.no {{ background: var(--earth); }}
/* Hand-drawn brush stroke, as if drawn on an iPad over the frame. */
.stroke {{ fill: none; stroke: var(--white); stroke-width: 16; stroke-linecap: round; stroke-linejoin: round; filter: url(#brush) drop-shadow(0 4px 10px rgba(10,10,10,.5)); }}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute"><filter id="brush"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="9"/></filter></svg>
<header>
<h1>{title}</h1>
<p>{summary}</p>
<label><input type="checkbox" onchange="document.body.classList.toggle('show-safe', this.checked)"> Mostrar zona segura de Instagram</label>
</header>
<main class="grid">
{beats}
</main>
</body>
</html>
"""

BEAT = """<article class="beat" id="beat-{id}">
<div class="screen"><div class="stage">
<img src="{frame}" alt="">
<div class="layer">{behind}</div>
{cutout}
<div class="layer">{front}</div>
{caption}
<div class="safe"></div>
</div></div>
<div class="meta">
<div class="time"><strong>{id}</strong> · {start:.2f}–{end:.2f}s</div>
<div class="said">«{said}»</div>
<div class="notes">{notes}</div>
</div>
</article>"""


def extract_frame(video, seconds, out_path):
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-ss", f"{seconds:.3f}", "-i", str(video),
         "-frames:v", "1", "-vf", "scale=1080:1920", "-q:v", "3", str(out_path)],
        check=True,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("reel", type=Path)
    parser.add_argument("--open", action="store_true", help="open the page in the browser")
    args = parser.parse_args()

    edit = args.reel / "edit"
    video = args.reel / "public" / "main_cut.mp4"
    spec = json.loads((edit / "storyboard.json").read_text())
    assets = edit / "storyboard"
    assets.mkdir(exist_ok=True)

    beats = []
    for beat in spec["beats"]:
        at = beat.get("at", (beat["from"] + beat["to"]) / 2)
        frame = assets / f"beat-{beat['id']:02}-{at:.2f}.jpg"
        if not frame.exists():
            extract_frame(video, at, frame)
        cutout = ""
        if beat.get("behind"):
            cut = assets / f"beat-{beat['id']:02}-{at:.2f}-cut.png"
            if not cut.exists():
                cut_out_frame(video, cut, at)
            cutout = f'<img src="storyboard/{cut.name}" alt="">'
        caption = beat.get("caption")
        beats.append(BEAT.format(
            id=beat["id"],
            frame=f"storyboard/{frame.name}",
            behind=beat.get("behind", ""),
            cutout=cutout,
            front=beat.get("front", ""),
            caption=f'<div class="caption">{caption}</div>' if caption else "",
            start=beat["from"],
            end=beat["to"],
            said=html.escape(beat.get("said", "")),
            notes=html.escape(beat.get("notes", "")),
        ))

    look = spec.get("look", {})
    page = edit / "storyboard.html"
    page.write_text(PAGE.format(
        title=html.escape(spec.get("title", args.reel.name)),
        summary=html.escape(spec.get("summary", "")),
        scale=PREVIEW_SCALE,
        beats="\n".join(beats),
    ).replace("var(--grade)", look.get("grade", "none")))
    print(f"wrote {page} ({len(beats)} beats)")
    if args.open:
        subprocess.run(["open", str(page)], check=True)


if __name__ == "__main__":
    main()
