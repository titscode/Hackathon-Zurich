#!/usr/bin/env python3
"""Capture la galerie index.html (cadre iPhone / tableau de bord) en PNG, pour le PR et la doc.

    python scripts/shot_gallery.py                      # 3 vues par defaut -> docs/gallery-*.png
    python scripts/shot_gallery.py 04-route 10-ride-mode-bike   # ids de RIDE_SEQUENCE (screens/features.js)

Viewport 1440x900 @2x. Les ecrans sont charges dans l'iframe : on attend leur networkidle avant la capture.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DEFAULT = ["04-route", "07-trip-swap", "09-segment", "tft-01-briefing"]


def main() -> None:
    ids = sys.argv[1:] or DEFAULT
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("erreur: playwright absent.\n  pip install playwright && python -m playwright install chromium")
    sys.path.insert(0, str(ROOT / "scripts"))
    from shot import chromium_path

    DOCS.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chromium_path())
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        page.goto((ROOT / "index.html").as_uri(), wait_until="networkidle")
        for i in ids:
            page.evaluate("id => window.showEntry(id)", i)
            page.wait_for_timeout(300)
            for fr in page.frames[1:]:
                fr.wait_for_load_state("networkidle")
            page.wait_for_timeout(700)          # cadrage Leaflet, fondus 200 ms
            dst = DOCS / f"gallery-{i}.png"
            page.screenshot(path=str(dst))
            print(f"index.html#{i} -> {dst.relative_to(ROOT)}")
        browser.close()


if __name__ == "__main__":
    main()
