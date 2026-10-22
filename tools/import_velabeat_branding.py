#!/usr/bin/env python3
"""Stage VelaBeat launcher artwork without overwriting BitChord icons."""
from pathlib import Path
from PIL import Image
import sys

root = Path.cwd()
assets = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("VelaBeat_Launcher_Assets")
source = assets / "velabeat_launcher_1024.png"
if not (root / "app/src/main/AndroidManifest.xml").is_file():
    raise SystemExit("Run from repository root")
if not source.is_file():
    raise SystemExit(f"Missing artwork: {source}")
image = Image.open(source).convert("RGBA")
if image.size != (1024, 1024):
    raise SystemExit(f"Unexpected dimensions: {image.size}")
emblem = image.crop((120, 75, 905, 760))
canvas = Image.new("RGBA", (1024, 1024), (9, 11, 37, 255))
emblem.thumbnail((780, 780), Image.Resampling.LANCZOS)
canvas.alpha_composite(emblem, ((1024-emblem.width)//2, (1024-emblem.height)//2))
for density, size in [("mdpi",48),("hdpi",72),("xhdpi",96),("xxhdpi",144),("xxxhdpi",192)]:
    directory = root / "app/src/main/res" / f"mipmap-{density}"
    directory.mkdir(parents=True, exist_ok=True)
    icon = canvas.resize((size,size), Image.Resampling.LANCZOS)
    icon.save(directory / "velabeat_launcher.png")
    icon.save(directory / "velabeat_launcher_round.png")
directory = root / "app/src/main/res/drawable-nodpi"
directory.mkdir(parents=True, exist_ok=True)
image.save(directory / "velabeat_brand_full.png")
print("Candidate assets staged. Existing launcher and adaptive icon mappings remain unchanged.")
