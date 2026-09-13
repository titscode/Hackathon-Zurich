#!/usr/bin/env python3
"""Exporte les mockups RIDE en PDF A4 paysage : page de garde, puis 4 maquettes par page (RIDE_SEQUENCE de
screens/features.js), chacune dans le cadre iPhone de design-system/iphone.css (cadre tableau de bord pour le TFT,
qui occupe deux emplacements), avec sous chaque maquette le numero de feature, le titre de l'ecran et l'etat.

    python scripts/export_pdf.py               # regenere les PNG (shot.py) puis docs/RIDE-mockups.pdf
    python scripts/export_pdf.py --no-shots    # utilise les PNG deja dans out/
    python scripts/export_pdf.py -o autre.pdf

Aucune dependance nouvelle : le PDF est imprime par Chromium (Playwright page.pdf), texte vectoriel, Inter vendorisee.
"""
import argparse
import datetime as dt
import html
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out"
DOCS = ROOT / "docs"
sys.path.insert(0, str(ROOT / "scripts"))
from shot import WIDTH, HEIGHT, SCALE, chromium_path, shoot  # noqa: E402

# A4 paysage 297 x 210 mm, 4 emplacements de 63 mm en ligne (marges 12 mm, gouttieres 6 mm).
PX = 96 / 25.4                                   # px CSS par mm
SLOT_MM, GAP_MM = 63, 6
PHONE_W, PHONE_H = 426, 880                      # cadre iPhone (iphone.css)
DASH_W, DASH_H = 842, 360                        # cadre tableau de bord + fixations
PHONE_SCALE = round(SLOT_MM * PX / PHONE_W, 4)   # ~0.56 -> 63 x 130 mm
DASH_SCALE = round((2 * SLOT_MM + GAP_MM) * PX / DASH_W, 4)
SLOTS = 4

CSS = f"""
@page {{ size: 297mm 210mm; margin: 0; }}
html, body {{ margin: 0; background: #0A0B0D; color: #F4F5F7; font-family: Inter, sans-serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ position: relative; width: 297mm; height: 210mm; overflow: hidden; page-break-after: always; box-sizing: border-box; }}
.page:last-child {{ page-break-after: auto; }}
.head, .foot {{ position: absolute; left: 12mm; right: 12mm; display: flex; justify-content: space-between; font-size: 10px; color: #5F6670; letter-spacing: 0.06em; }}
.head {{ top: 10mm; }}
.foot {{ bottom: 9mm; }}
.head b {{ font-weight: 500; color: #9AA0A8; letter-spacing: 0; }}
.row {{ position: absolute; left: 12mm; right: 12mm; top: 18mm; bottom: 16mm; display: flex; gap: {GAP_MM}mm; align-items: center; justify-content: flex-start; }}
.slot {{ width: {SLOT_MM}mm; flex: none; display: flex; flex-direction: column; align-items: center; }}
.slot.wide {{ width: {2 * SLOT_MM + GAP_MM}mm; }}
.fit {{ transform-origin: 0 0; }}
.cap {{ margin-top: 5mm; text-align: center; width: 100%; }}
.cap .feat {{ font-size: 10px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; color: #5F6670; }}
.cap .title {{ font-size: 14px; font-weight: 600; margin-top: 4px; line-height: 1.2; }}
.cap .state {{ font-size: 11px; color: #9AA0A8; margin-top: 3px; }}
/* page de garde */
.cover .brand {{ position: absolute; left: 16mm; top: 40mm; }}
.cover .brand .logo {{ font-size: 44px; font-weight: 600; letter-spacing: 0.02em; }}
.cover .brand .by {{ font-size: 12px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; color: #5F6670; margin-top: 6px; }}
.cover .brand .tag {{ font-size: 20px; color: #9AA0A8; margin-top: 28px; }}
.cover .meta {{ position: absolute; left: 16mm; bottom: 24mm; font-size: 12px; color: #5F6670; line-height: 1.6; }}
.cover .list {{ position: absolute; left: 150mm; top: 34mm; width: 130mm; }}
.cover .list h2 {{ font-size: 11px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; color: #5F6670; margin: 0 0 10px; }}
.cover .list ol {{ margin: 0; padding: 0; list-style: none; }}
.cover .list li {{ display: flex; gap: 12px; font-size: 13px; line-height: 1.4; padding: 7px 0; border-top: 1px solid #262A31; }}
.cover .list li span:first-child {{ color: #5F6670; font-size: 11px; font-weight: 500; letter-spacing: 0.08em; width: 22px; flex: none; padding-top: 2px; }}
"""

PHONE_MARKUP = ('<div class="iphone">'
                '<i class="k action"></i><i class="k vol-up"></i><i class="k vol-down"></i><i class="k power"></i>'
                '<i class="ant tl"></i><i class="ant tr"></i><i class="ant bl"></i><i class="ant br"></i>'
                '<div class="screen-wrap"><div class="island"></div><img src="{png}" alt=""></div></div>')
DASH_MARKUP = '<div class="dash"><div class="screen-wrap"><img src="{png}" alt=""></div></div>'


def slot_html(e):
    png = (OUT / f"{e['id']}.png").as_uri()
    if e.get("tft"):
        scale, box_w, box_h = DASH_SCALE, DASH_W, DASH_H
        mock, wide, state = DASH_MARKUP.format(png=png), " wide", 'As shown on the bike\'s 10.25" TFT'
    else:
        scale, box_w, box_h = PHONE_SCALE, PHONE_W, PHONE_H
        mock, wide, state = PHONE_MARKUP.format(png=png), "", e["state"]
    box = f"width:{box_w * scale:.0f}px;height:{box_h * scale:.0f}px"
    return f"""
  <div class="slot{wide}">
    <div class="fit" style="{box};transform:scale({scale})">{mock}</div>
    <div class="cap"><div class="feat">Feature {e['feature']:02d}</div><div class="title">{html.escape(e['title'])}</div>
      {f'<div class="state">{html.escape(state)}</div>' if state else ''}</div>
  </div>"""


def paginate(seq):
    """Groupes de 4 emplacements ; le TFT en prend 2 et passe a la page suivante s'il ne reste pas la place."""
    pages, cur, used = [], [], 0
    for e in seq:
        w = 2 if e.get("tft") else 1
        if used + w > SLOTS:
            pages.append(cur)
            cur, used = [], 0
        cur.append(e)
        used += w
    if cur:
        pages.append(cur)
    return pages


def page_html(entries, i, n):
    feats = sorted({e["feature"] for e in entries})
    rng = f"Feature {feats[0]:02d}" if len(feats) == 1 else f"Features {feats[0]:02d} to {feats[-1]:02d}"
    screens = ", ".join(e["src"].split(".")[0] for e in entries)
    return f"""
<section class="page">
  <div class="head"><span><b>RIDE by BMW Motorrad</b> · Mockups</span><span>{rng}</span></div>
  <div class="row">{''.join(slot_html(e) for e in entries)}</div>
  <div class="foot"><span>Screens {html.escape(screens)}</span><span>{i} / {n}</span></div>
</section>"""


def cover_html(seq, feats, n):
    screens = len({e["src"].split(".")[0] for e in seq})
    items = "".join(f'<li><span>{f["n"]:02d}</span><span>{html.escape(f["title"])}</span></li>' for f in feats)
    return f"""
<section class="page cover">
  <div class="brand"><div class="logo">RIDE</div><div class="by">by BMW Motorrad</div><div class="tag">Find your best road.</div></div>
  <div class="list"><h2>Ten features</h2><ol>{items}</ol></div>
  <div class="meta">Mockups · {screens} screens, {len(seq)} states · {dt.date.today().strftime('%d %b %Y')}<br>Hackathon Zurich · DESIGN.md and SCREENS.md are the source of truth</div>
  <div class="foot"><span>RIDE by BMW Motorrad · Mockups</span><span>0 / {n}</span></div>
</section>"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default=str(DOCS / "RIDE-mockups.pdf"))
    ap.add_argument("--no-shots", action="store_true", help="ne pas regenerer les PNG de out/")
    args = ap.parse_args()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("erreur: playwright absent.\n  pip install playwright && python -m playwright install chromium")

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chromium_path())
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=SCALE)
        page.goto("about:blank")
        page.add_script_tag(path=str(ROOT / "screens" / "features.js"))
        seq = page.evaluate("RIDE_SEQUENCE")
        feats = page.evaluate("RIDE_FEATURES")

        if not args.no_shots:
            OUT.mkdir(exist_ok=True)
            for e in seq:
                # id = nom du PNG ("06-voice-live") ; shot.py attend "06-voice#live". Quand la galerie joue
                # l'animation (src sans hash), l'etat fige du PDF est le dernier segment de l'id.
                name = e["src"].replace(".html", "")
                if name.replace("#", "-") != e["id"]:
                    name = "#".join(e["id"].rsplit("-", 1))
                shoot(page, name, False)

        pages = paginate(seq)
        n = len(pages)
        doc = ("<!doctype html><html><head><meta charset='utf-8'>"
               f"<link rel='stylesheet' href='{(ROOT / 'design-system' / 'fonts' / 'inter.css').as_uri()}'>"
               f"<link rel='stylesheet' href='{(ROOT / 'design-system' / 'iphone.css').as_uri()}'>"
               f"<style>{CSS}</style></head><body>"
               + cover_html(seq, feats, n)
               + "".join(page_html(entries, i + 1, n) for i, entries in enumerate(pages))
               + "</body></html>")
        tmp = Path(tempfile.gettempdir()) / "ride-mockups.html"
        tmp.write_text(doc, encoding="utf-8")

        pdf = browser.new_page(viewport={"width": 1123, "height": 794})
        pdf.goto(tmp.as_uri(), wait_until="networkidle")
        pdf.wait_for_timeout(300)
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        pdf.pdf(path=args.out, format="A4", landscape=True, print_background=True, prefer_css_page_size=True)
        browser.close()
    size = Path(args.out).stat().st_size // 1024
    print(f"{args.out} : {n + 1} pages (garde + {n}), {len(seq)} maquettes, {size} Ko")


if __name__ == "__main__":
    main()
