from pathlib import Path
from PIL import Image

SRC = Path("photos")
OUT = SRC

JOBS = [
    # (source, new hero file, focus "top" or "center")
    ("card-worship.webp", "hero-story.webp", "top"),
    ("card-pastor.webp", "hero-pastor.webp", "top"),
    ("card-celebration.webp", "hero-testimonies.webp", "top"),
    ("card-community.webp", "hero-impact.webp", "top"),
    ("card-welcome.webp", "hero-attend.webp", "top"),
    ("card-graduation.webp", "hero-library.webp", "top"),
    ("card-music.webp", "hero-conference.webp", "top"),
]

W, H = 1280, 720

for src, dst, focus in JOBS:
    p = SRC / src
    if not p.exists():
        print("missing", src)
        continue
    im = Image.open(p).convert("RGB")
    w, h = im.size
    target_ratio = W / H
    src_ratio = w / h
    if src_ratio > target_ratio:
        # crop width
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        box = (left, 0, left + new_w, h)
    else:
        new_h = int(w / target_ratio)
        if focus == "top":
            top = 0
        else:
            top = max(0, (h - new_h) // 2)
        box = (0, top, w, top + new_h)
    out = im.crop(box).resize((W, H), Image.LANCZOS)
    out.save(OUT / dst, "WEBP", quality=78, method=6)
    print("wrote", dst, (OUT / dst).stat().st_size // 1024, "KB")

# Social share image 1200x630
im = Image.open(SRC / "hero-about.webp").convert("RGB")
w, h = im.size
ratio = 1200 / 630
if w / h > ratio:
    new_w = int(h * ratio)
    left = (w - new_w) // 2
    im = im.crop((left, 0, left + new_w, h))
else:
    new_h = int(w / ratio)
    top = (h - new_h) // 2
    im = im.crop((0, top, w, top + new_h))
im = im.resize((1200, 630), Image.LANCZOS)
im.save("og-rpai.jpg", "JPEG", quality=86, optimize=True)
print("wrote og-rpai.jpg", Path("og-rpai.jpg").stat().st_size // 1024, "KB")
