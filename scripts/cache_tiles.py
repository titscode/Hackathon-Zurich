#!/usr/bin/env python3
"""Met en cache localement les tuiles de carte qu'un ecran demande.

Les ecrans referencent ../design-system/tiles/<fournisseur>/{z}/{x}/{y}.png (hors-ligne,
deterministe). Le fournisseur est choisi ici et publie dans design-system/tiles/source.js,
lu par rideTileLayer() (screens/data.js) :

  - MAPTILER_KEY definie -> MapTiler "dataviz-dark" (deja sombre ; image 512 px sur grille 256,
                            nette sur le PNG @2x, tileSize 256 / zoomOffset 0 comme OSM)
  - sinon                -> OSM : brut dans tiles/_raw/osm (jamais servi), puis labels gommes
                            par Pillow dans tiles/osm (servi) et assombri par le filtre CSS .map-osm

    python scripts/cache_tiles.py 04-route
    python scripts/cache_tiles.py "08-explore#heat"
    python scripts/cache_tiles.py 07-trip --refresh      # re-telecharge meme si deja en cache
    python scripts/cache_tiles.py --reprocess            # regenere tiles/osm depuis tiles/_raw/osm
    python scripts/cache_tiles.py 04-route --provider osm

Windows : setx MAPTILER_KEY "..." puis rouvrir le terminal. Jamais de cle dans un fichier du repo.
"""
import argparse
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TILES = ROOT / "design-system" / "tiles"
RAW = TILES / "_raw"
UA = "RIDE-mockup/1.0 (hackathon prototype; github.com/titscode/Hackathon-Zurich)"
PAT = re.compile(r"/design-system/tiles/([a-z0-9-]+)/(\d+)/(\d+)/(\d+)\.png")

# Preparation des tuiles OSM pour le filtre CSS .map-osm
# (invert(1) hue-rotate(180deg) saturate(0.2) brightness(0.45) contrast(1.25)).
# Bump FLATTEN_VERSION + --reprocess quand l'algo change.
FLATTEN_VERSION = 2
INK_MAX = 140        # luminance en dessous de laquelle un pixel est de l'encre (glyphes noirs, rails, frontieres)
INK_GRAY_MAX = 185   # ... ou un gris peu sature (noms de regions, casings), sans toucher aux routes colorees
INK_GRAY_SAT = 40    # saturation HSV (0-255) sous laquelle un pixel compte comme gris
INK_DILATE = 5       # dilatation du masque, couvre le halo blanc autour des glyphes
FILL_MEDIAN = 9      # taille du median qui fabrique le fond de remplacement
TONE = 0.68          # assombrit la source : apres inversion + brightness(.45), contrast(1.25) (pivot 50 %)
                     # ecraserait un fond clair en noir pur ; avec 0.68 le sol ressort vers surface-1 (~L19),
                     # eau ~L38, forets ~L42
ROAD_GRAY = 73       # routes OSM blanches -> ce gris, qui devient ~L70 apres le filtre : routes claires sur sol sombre

PROVIDERS = {
    "osm": dict(
        src="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        maxZoom=19, dark=False, flatten=True,
    ),
    "dataviz-dark": dict(
        src="https://api.maptiler.com/maps/dataviz-dark/256/{z}/{x}/{y}@2x.png?key={key}",
        maxZoom=22, dark=True, flatten=False,
    ),
}

sys.path.insert(0, str(ROOT / "scripts"))
from shot import chromium_path, SCREENS, WIDTH, HEIGHT, SCALE  # noqa: E402


def pick_provider(forced):
    if forced:
        return forced
    if os.environ.get("MAPTILER_KEY"):
        return "dataviz-dark"
    print("MAPTILER_KEY absente -> OSM (labels gommes par Pillow, filtre CSS .map-osm)")
    return "osm"


def write_source_js(provider):
    p = PROVIDERS[provider]
    js = (
        "/* Genere par scripts/cache_tiles.py, ne pas editer. Aucune cle ici. */\n"
        f'window.TILES = {{ provider: "{provider}", url: "../design-system/tiles/{provider}/{{z}}/{{x}}/{{y}}.png",\n'
        f"                 tileSize: 256, zoomOffset: 0, maxZoom: {p['maxZoom']}, dark: {'true' if p['dark'] else 'false'} }};\n"
    )
    dst = TILES / "source.js"
    if not dst.exists() or dst.read_text(encoding="utf-8") != js:
        dst.write_text(js, encoding="utf-8")
        print(f"design-system/tiles/source.js -> {provider}")


def flatten_osm(im):
    """Prepare une tuile OSM pour le filtre CSS .map-osm : labels gommes, ton abaisse, routes relevees.

    1. Gomme a encre : masque des glyphes (noirs, ou gris peu satures pour les noms de regions),
       dilate, rempli par un median large. Un median 3x3 nu laisse des taches sur les labels gras
       et amincit les routes ; le CSS seul ne retire rien (apres inversion les glyphes sont ce qu'il
       y a de plus clair sur la tuile).
    2. Routes blanches -> gris ROAD_GRAY, pour qu'elles ressortent en clair apres inversion
       (sinon sol et routes, tous deux clairs, deviennent tous deux noirs).
    3. Ton x TONE, pour que contrast(1.25) n'ecrase pas le sol inverse en noir pur.
    """
    from PIL import Image, ImageChops, ImageFilter

    rgb = im.convert("RGB")                       # tuiles OSM en mode P (palette)
    lum = rgb.convert("L")
    sat = rgb.convert("HSV").getchannel("S")
    ink = lum.point(lambda v: 255 if v < INK_MAX else 0)
    gray = ImageChops.multiply(lum.point(lambda v: 255 if v < INK_GRAY_MAX else 0),
                               sat.point(lambda v: 255 if v < INK_GRAY_SAT else 0))
    mask = ImageChops.lighter(ink, gray).filter(ImageFilter.MaxFilter(INK_DILATE))
    fill = rgb.filter(ImageFilter.MedianFilter(FILL_MEDIAN))
    out = Image.composite(fill, rgb, mask)

    r, g, b = out.split()
    white = ImageChops.multiply(ImageChops.multiply(r.point(lambda v: 255 if v >= 248 else 0),
                                                    g.point(lambda v: 255 if v >= 248 else 0)),
                                b.point(lambda v: 255 if v >= 248 else 0))
    out = out.point(lambda v: int(v * TONE))
    return Image.composite(Image.new("RGB", out.size, (ROAD_GRAY,) * 3), out, white)


def raw_path(provider, z, x, y):
    base = RAW / provider if PROVIDERS[provider]["flatten"] else TILES / provider
    return base / str(z) / str(x) / f"{y}.png"


def fetch(provider, z, x, y, refresh):
    """Telecharge la tuile brute si absente. Ne logue jamais l'URL (elle porte la cle)."""
    dst = raw_path(provider, z, x, y)
    if dst.exists() and not refresh:
        return dst, False
    url = PROVIDERS[provider]["src"].format(z=z, x=x, y=y, key=os.environ.get("MAPTILER_KEY", ""))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        hint = " (cle MapTiler invalide ?)" if e.code in (401, 403) else ""
        sys.exit(f"erreur: HTTP {e.code} pour {provider} {z}/{x}/{y}{hint}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(data)
    return dst, True


def publish(provider, z, x, y):
    """Rend la tuile servable : OSM passe par la gomme a encre, MapTiler est servi tel quel."""
    src = raw_path(provider, z, x, y)
    if not PROVIDERS[provider]["flatten"]:
        return src
    from PIL import Image

    dst = TILES / provider / str(z) / str(x) / f"{y}.png"
    dst.parent.mkdir(parents=True, exist_ok=True)
    flatten_osm(Image.open(src)).save(dst, optimize=True)
    return dst


def reprocess(provider):
    n = 0
    for src in sorted((RAW / provider).glob("*/*/*.png")):
        z, x, y = src.parent.parent.name, src.parent.name, src.stem
        publish(provider, z, x, y)
        n += 1
    print(f"{n} tuile(s) {provider} regeneree(s) depuis tiles/_raw/{provider} (flatten v{FLATTEN_VERSION})")


def missing_tiles(name, state):
    src = SCREENS / f"{name}.html"
    if not src.exists():
        sys.exit(f"erreur: {src} introuvable")
    from playwright.sync_api import sync_playwright

    found = set()

    def note(url):
        m = PAT.search(url)
        if m:
            found.add((m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))))

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chromium_path())
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=SCALE)
        page.on("requestfailed", lambda r: note(r.url))
        page.on("response", lambda r: r.status >= 400 and note(r.url))
        page.goto(src.as_uri() + (f"#{state}" if state else ""), wait_until="networkidle")
        page.wait_for_timeout(600)
        browser.close()
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("screen", nargs="?", help="nom de l'ecran, avec #etat optionnel (ex: 08-explore#heat)")
    ap.add_argument("--provider", choices=PROVIDERS, help="force le fournisseur (defaut: MAPTILER_KEY ? dataviz-dark : osm)")
    ap.add_argument("--refresh", action="store_true", help="re-telecharge les tuiles deja en cache")
    ap.add_argument("--reprocess", action="store_true", help="regenere tiles/osm depuis tiles/_raw/osm")
    args = ap.parse_args()

    provider = pick_provider(args.provider)
    write_source_js(provider)

    if args.reprocess:
        reprocess("osm")
    if not args.screen:
        if not args.reprocess:
            ap.error("donne un ecran ou --reprocess")
        return

    name, _, state = args.screen.partition("#")
    todo = missing_tiles(name, state)
    foreign = sorted({t[0] for t in todo if t[0] != provider})
    if foreign:
        sys.exit(f"erreur: l'ecran demande des tuiles {foreign} alors que source.js dit {provider}. "
                 "Verifie que l'ecran passe par rideTileLayer() (data.js).")
    print(f"{len(todo)} tuile(s) manquante(s)")
    for _, z, x, y in sorted(todo):
        _, downloaded = fetch(provider, z, x, y, args.refresh)
        out = publish(provider, z, x, y)
        print(f"  {provider} {z}/{x}/{y}  {'telechargee' if downloaded else 'brute en cache'}  ({out.stat().st_size // 1024} Ko)")


if __name__ == "__main__":
    main()
