"""Create lightweight slideshow thumbnails for the photos in gallery.html.

The slideshow shows photographs in a 4:3 frame, so each thumbnail is centre
cropped to 4:3 and saved as WebP. The original file is left untouched and the
lightbox link keeps pointing at it, so tapping a photo still opens the full
resolution version.

Run from anywhere:

    python scripts/make-gallery-thumbs.py

Re-running is safe: photos that already use a thumbnail are skipped.
"""

import hashlib
import re
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "gallery.html"
START = "<!-- rpai:gallery:start -->"
END = "<!-- rpai:gallery:end -->"
THUMB_DIR = ROOT / "photos" / "gallery-thumbs"
THUMB_PREFIX = "photos/gallery-thumbs/"
MAX_WIDTH = 640
QUALITY = 78

THUMB_DIR.mkdir(parents=True, exist_ok=True)

with open(HTML, "r", encoding="utf-8", newline="") as handle:
    text = handle.read()

start_at = text.index(START) + len(START)
end_at = text.index(END)
block = text[start_at:end_at]

used = {}
before_bytes = 0
after_bytes = 0
made = 0
reused = 0
skipped = 0


def thumb_for(src: str) -> str:
    global made, reused, before_bytes, after_bytes

    original = ROOT / src
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", original.stem).strip("-").lower() or "photo"
    if stem in used and used[stem] != src:
        stem = f"{stem}-{hashlib.md5(src.encode('utf-8')).hexdigest()[:6]}"
    used[stem] = src
    out = THUMB_DIR / f"{stem}.webp"
    rel = f"{THUMB_PREFIX}{stem}.webp"

    before_bytes += original.stat().st_size

    if out.is_file():
        reused += 1
        after_bytes += out.stat().st_size
        return rel

    with Image.open(original) as picture:
        picture = ImageOps.exif_transpose(picture)
        picture = picture.convert("RGB")
        width, height = picture.size
        target = 4 / 3
        if width / height > target:
            new_width = int(height * target)
            left = (width - new_width) // 2
            picture = picture.crop((left, 0, left + new_width, height))
        else:
            new_height = int(width / target)
            top = (height - new_height) // 2
            picture = picture.crop((0, top, width, top + new_height))
        width, height = picture.size
        if width > MAX_WIDTH:
            picture = picture.resize(
                (MAX_WIDTH, int(MAX_WIDTH / target)), Image.Resampling.LANCZOS
            )
        picture.save(out, "WEBP", quality=QUALITY, method=6)

    made += 1
    after_bytes += out.stat().st_size
    return rel


def replace_img(match: re.Match) -> str:
    global skipped

    tag = match.group(0)
    src_match = re.search(r'src="([^"]+)"', tag)
    if not src_match:
        return tag
    src = src_match.group(1)
    if src.startswith(("http://", "https://", "data:", THUMB_PREFIX)):
        skipped += 1
        return tag
    if not (ROOT / src).is_file():
        print(f"  skip (missing): {src}")
        return tag

    thumb = thumb_for(src)
    return tag[: src_match.start(1)] + thumb + tag[src_match.end(1):]


new_block, count = re.subn(r"<img\b[^>]*>", replace_img, block)
new_text = text[:start_at] + new_block + text[end_at:]

if new_text != text:
    with open(HTML, "w", encoding="utf-8", newline="") as handle:
        handle.write(new_text)

print(f"images checked   : {count}")
print(f"thumbnails made  : {made} (reused {reused}, already done {skipped})")
if before_bytes:
    print(f"originals        : {before_bytes / 1024:.0f} KB")
    print(f"thumbnails       : {after_bytes / 1024:.0f} KB")
    print(f"saved            : {(before_bytes - after_bytes) / 1024:.0f} KB "
          f"({100 * (before_bytes - after_bytes) / before_bytes:.1f}%)")
print(f"thumb dir        : {THUMB_DIR}")
