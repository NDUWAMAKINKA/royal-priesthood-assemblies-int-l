"""
Generate small responsive variants for the site images.

For every card-*.webp we write:
  thumb-<name>.webp  (640px wide)  - already exists for most, regenerated here
  quick-<name>.webp  (420px wide)

Heroes get a single 960px variant: hero-<name>-960.webp
"""
from pathlib import Path
from PIL import Image

SRC = Path("photos")


def resize(src: Path, dst: Path, width: int, quality: int = 74) -> None:
    im = Image.open(src).convert("RGB")
    if im.width <= width:
        im.save(dst, "WEBP", quality=quality, method=6)
        return
    w, h = im.size
    new_h = max(1, round(h * width / w))
    out = im.resize((width, new_h), Image.LANCZOS)
    out.save(dst, "WEBP", quality=quality, method=6)


count = 0
for card in sorted(SRC.glob("card-*.webp")):
    base = card.stem.replace("card-", "")
    resize(card, SRC / f"thumb-{base}.webp", 640)
    resize(card, SRC / f"quick-{base}.webp", 420)
    count += 1

for hero in sorted(SRC.glob("hero-*.webp")):
    if "-960" in hero.stem:
        continue
    resize(hero, SRC / f"{hero.stem}-960.webp", 960, 78)
    count += 1

print(f"wrote {count * 2} variants")
