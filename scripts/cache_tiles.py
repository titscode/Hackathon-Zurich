#!/usr/bin/env python3
"""Met en cache localement les tuiles de carte qu'un ecran demande.

Les ecrans referencent ../design-system/tiles/{z}/{x}/{y}.png (hors-ligne,
deterministe). Ce script ouvre l'ecran, note les tuiles manquantes et les
telecharge depuis CartoDB.

    python scripts/cache_tiles.py 04-route
    python scripts/cache_tiles.py 08-explore#heat
"""
import re, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TILES = ROOT / "design-system" / "tiles"
# CartoDB Dark Matter exige desormais une cle API (tuiles filigranees) : on prend OSM
# et on l'assombrit par filtre CSS dans les ecrans (voir 04-route.html).
SRC = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
UA = "RIDE-mockup/1.0 (hackathon prototype; github.com/titscode/Hackathon-Zurich)"
PAT = re.compile(r"/design-system/tiles/(\d+)/(\d+)/(\d+)\.png")

sys.path.insert(0, str(ROOT / "scripts"))
from shot import chromium_path, SCREENS, WIDTH, HEIGHT, SCALE  # noqa: E402

name, _, state = sys.argv[1].partition("#")
src = SCREENS / f"{name}.html"
if not src.exists():
    sys.exit(f"erreur: {src} introuvable")

from playwright.sync_api import sync_playwright

missing = set()
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=chromium_path())
    page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=SCALE)
    page.on("requestfailed", lambda r: (m := PAT.search(r.url)) and missing.add(tuple(map(int, m.groups()))))
    page.on("response", lambda r: r.status >= 400 and (m := PAT.search(r.url)) and missing.add(tuple(map(int, m.groups()))))
    page.goto(src.as_uri() + (f"#{state}" if state else ""), wait_until="networkidle")
    page.wait_for_timeout(600)
    browser.close()

print(f"{len(missing)} tuile(s) manquante(s)")
for i, (z, x, y) in enumerate(sorted(missing)):
    dst = TILES / str(z) / str(x) / f"{y}.png"
    dst.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(SRC.format(z=z, x=x, y=y), headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        dst.write_bytes(r.read())
    print(f"  {z}/{x}/{y}  ({dst.stat().st_size // 1024} Ko)")
