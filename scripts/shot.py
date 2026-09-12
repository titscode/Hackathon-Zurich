#!/usr/bin/env python3
"""Screenshot un mockup HTML en PNG via Playwright.

    python scripts/shot.py home              # screens/home.html -> out/home.png
    python scripts/shot.py home --full-page
    python scripts/shot.py --all
"""
import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCREENS = ROOT / "screens"
OUT = ROOT / "out"

WIDTH, HEIGHT = 390, 844
SCALE = 2


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
    """Echoue si Tailwind n'a pas ete applique.

    Sans ce garde-fou, un script non charge produit un PNG non style sans
    aucune erreur, et on ne s'en apercoit qu'a l'oeil.
    """
    ok = page.evaluate(
        """() => {
            const el = document.querySelector('[class*="w-["], [class*="flex"], [class*="px-"]');
            if (!el) return true;
            const cs = getComputedStyle(el);
            return cs.display === 'flex' || cs.paddingLeft !== '0px' || cs.width !== 'auto';
        }"""
    )
    if not ok:
        sys.exit(
            f"erreur: les styles Tailwind ne sont pas appliques sur {name}.\n"
            "  Verifie <script src=\"../design-system/tailwind.js\"></script> dans le HTML."
        )


def shoot(page, name: str, full_page: bool) -> Path:
    src = SCREENS / f"{name}.html"
    if not src.exists():
        sys.exit(f"erreur: {src} introuvable")
    dst = OUT / f"{name}.png"
    page.goto(src.as_uri(), wait_until="networkidle")
    # Tailwind s'injecte apres le parse: laisser un tick de plus.
    page.wait_for_timeout(400)
    assert_styled(page, name)
    page.screenshot(path=str(dst), full_page=full_page)
    print(f"{src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
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
