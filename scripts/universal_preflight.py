#!/usr/bin/env python3
"""Read-only preflight for a future single-package VelaBeat APK."""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
mobile = root / "app/src/main/java"
tv = root / "tv/src/main/java"
android_ns = "{http://schemas.android.com/apk/res/android}"
issues = []

def manifest(path):
    return ET.parse(root / path).getroot()

def launcher_categories(tree):
    found = []
    for kind in ("activity", "activity-alias"):
        for node in tree.iter(kind):
            categories = {x.get(android_ns + "name") for x in node.iter("category")}
            if "android.intent.category.LAUNCHER" in categories or "android.intent.category.LEANBACK_LAUNCHER" in categories:
                found.append((kind, node.get(android_ns + "name"), sorted(categories)))
    return found

for label, path in (("mobile", "app/src/main/AndroidManifest.xml"), ("tv", "tv/src/main/AndroidManifest.xml")):
    tree = manifest(path)
    print(f"\n[{label} launcher entries]")
    for kind, name, cats in launcher_categories(tree):
        print(f"  {kind} {name}: {', '.join(cats)}")

mobile_paths = {p.relative_to(mobile).as_posix() for p in mobile.rglob("*.kt")}
tv_paths = {p.relative_to(tv).as_posix() for p in tv.rglob("*.kt")}
overlap = sorted(mobile_paths & tv_paths)
only_tv = sorted(tv_paths - mobile_paths)
print(f"\nMobile Kotlin files: {len(mobile_paths)}")
print(f"TV Kotlin files: {len(tv_paths)}")
print(f"TV-only Kotlin files: {len(only_tv)}")
print(f"Overridden Kotlin paths: {len(overlap)}")
print("\n[TV overrides: must resolve before merging source trees]")
for name in overlap:
    print("  " + name)
print("\n[TV-only Kotlin paths]")
for name in only_tv:
    print("  " + name)

for label, path, expected in (
    ("mobile", "app/build.gradle.kts", "net.velalab.velabeat.dev"),
    ("tv", "tv/build.gradle.kts", "net.velalab.velabeat.tv.dev"),
):
    text = (root / path).read_text()
    if f'applicationId = "{expected}"' not in text:
        issues.append(f"{label} dev applicationId differs from {expected}")
    if f'"-f", "{expected}"' not in text:
        issues.append(f"{label} verifyDevInstall still targets wrong package")

if not (root / "tv/src/main/java/com/music/bitchord/TvActivity.kt").exists():
    issues.append("TV Activity source missing")
if not (root / "tv/src/main/java/com/music/bitchord/ui/tv/TvApp.kt").exists():
    issues.append("TV Compose root missing")

print("\n[preflight]")
if issues:
    for item in issues:
        print("ERROR: " + item, file=sys.stderr)
    sys.exit(1)
print("PASS: existing package and TV entry-point invariants")
print("NOTE: this is NOT a universal APK build or device compatibility test")
