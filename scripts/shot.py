#!/usr/bin/env python3
"""Screenshot un mockup HTML en PNG via Playwright.

    python scripts/shot.py home              # screens/home.html -> out/home.png
    python scripts/shot.py home --full-page
    python scripts/shot.py --all
"""
import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCREENS = ROOT / "screens"
OUT = ROOT / "out"

WIDTH, HEIGHT = 390, 844
SCALE = 2
# Tuiles de carte servies hors-ligne (voir scripts/cache_tiles.py) : une tuile absente = PNG a trous.
TILE_PAT = re.compile(r"/design-system/tiles/[a-z0-9-]+/\d+/\d+/\d+\.png")


def chromium_path():
    """Chromium a utiliser. None = celui que playwright a installe (cas normal).

    CHROMIUM_PATH force un binaire precis ; sinon on repere un chromium deja
    present dans PLAYWRIGHT_BROWSERS_PATH quand sa version ne correspond pas a
    celle que ce playwright attend (cas des conteneurs pre-equipes).
    """
    explicit = os.environ.get("CHROMIUM_PATH")
    if explicit:
        return explicit
    browsers = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    if not browsers:
        return None
    for candidate in sorted(Path(browsers).glob("chromium-*/chrome-linux/chrome")):
        return str(candidate)
    return None


def assert_styled(page, name: str) -> None:
    """Echoue si aucune feuille de style n'a ete appliquee.

    Sans ce garde-fou, un CSS non charge (tokens.css absent, Tailwind bloque)
    produit un PNG non style sans aucune erreur, et on ne s'en apercoit qu'a l'oeil.
    """
    ok = page.evaluate(
        """() => {
            const bg = getComputedStyle(document.body).backgroundColor;
            const styled = bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'rgb(255, 255, 255)';
            const sheets = Array.from(document.styleSheets).some(s => { try { return s.cssRules.length > 0 } catch (e) { return true } });
            return styled && sheets;
        }"""
    )
    if not ok:
        sys.exit(
            f"erreur: aucun style applique sur {name}.\n"
            "  Verifie le <link> vers ../design-system/tokens.css (ou le <script> Tailwind) dans le HTML."
        )


def shoot(page, name: str, full_page: bool) -> Path:
    # "08-explore#heat" capture l'etat #heat de l'ecran dans out/08-explore-heat.png
    name, _, state = name.partition("#")
    src = SCREENS / f"{name}.html"
    if not src.exists():
        sys.exit(f"erreur: {src} introuvable")
    dst = OUT / (f"{name}-{state}.png" if state else f"{name}.png")
    missing = []
    on_failed = lambda r: TILE_PAT.search(r.url) and missing.append(r.url)
    page.on("requestfailed", on_failed)
    page.goto(src.as_uri() + (f"#{state}" if state else ""), wait_until="networkidle")
    # Tailwind s'injecte apres le parse: laisser un tick de plus.
    page.wait_for_timeout(400)
    assert_styled(page, name)
    page.screenshot(path=str(dst), full_page=full_page)
    page.remove_listener("requestfailed", on_failed)
    print(f"{src.relative_to(ROOT)}{'#' + state if state else ''} -> {dst.relative_to(ROOT)}")
    if missing:
        print(f"  ATTENTION: {len(missing)} tuile(s) de carte manquante(s), le PNG a des trous."
              f" Lance : python scripts/cache_tiles.py \"{name}{'#' + state if state else ''}\"")
    return dst


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("name", nargs="?", help="nom de l'ecran sans .html")
    ap.add_argument("--all", action="store_true", help="tous les ecrans de screens/")
    ap.add_argument("--full-page", action="store_true", help="capture la page entiere")
    args = ap.parse_args()

    if not args.all and not args.name:
        ap.error("donne un nom d'ecran ou --all")

    names = (
        sorted(p.stem for p in SCREENS.glob("*.html")) if args.all else [args.name]
    )
    if not names:
        sys.exit("erreur: aucun fichier .html dans screens/")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit(
            "erreur: playwright absent.\n"
            "  pip install playwright && python -m playwright install chromium"
        )

    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chromium_path())
        page = browser.new_page(
            viewport={"width": WIDTH, "height": HEIGHT},
            device_scale_factor=SCALE,
        )
        for name in names:
            shoot(page, name, args.full_page)
        browser.close()


if __name__ == "__main__":
    main()
