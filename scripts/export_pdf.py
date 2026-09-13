#!/usr/bin/env python3
"""Exporte les mockups RIDE en PDF A4 paysage : page de garde, puis une page par ecran et par etat
(RIDE_SEQUENCE de screens/features.js), mockup centre dans le cadre iPhone de design-system/iphone.css
(cadre tableau de bord pour le TFT), titre de l'ecran et numero de feature en marge.

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

# A4 paysage 297 x 210 mm. Cadre iPhone 414 x 868 px ramene a 172 mm de haut (96 px/in) : echelle 0.749.
PAGE_W, PAGE_H = 297, 210
PHONE_SCALE = round(172 / 25.4 * 96 / 868, 4)
DASH_SCALE = round(170 / 25.4 * 96 / 842, 4)      # cadre 842 px de large -> 170 mm

CSS = """
@page { size: 297mm 210mm; margin: 0; }
html, body { margin: 0; background: #0A0B0D; color: #F4F5F7; font-family: Inter, sans-serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { position: relative; width: 297mm; height: 210mm; overflow: hidden; page-break-after: always; box-sizing: border-box; }
.page:last-child { page-break-after: auto; }
.margin { position: absolute; left: 16mm; top: 18mm; width: 62mm; }
.margin .feat { font-size: 11px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; color: #5F6670; }
.margin .title { font-size: 22px; font-weight: 600; letter-spacing: -0.01em; margin-top: 8px; line-height: 1.2; }
.margin .state { font-size: 13px; color: #9AA0A8; margin-top: 6px; }
.margin .ftitle { font-size: 12px; color: #9AA0A8; margin-top: 22px; line-height: 1.45; padding-top: 14px; border-top: 1px solid #262A31; }
.margin .file { font-size: 11px; color: #5F6670; margin-top: 8px; }
.foot { position: absolute; left: 16mm; right: 16mm; bottom: 12mm; display: flex; justify-content: space-between; font-size: 10px; color: #5F6670; letter-spacing: 0.06em; }
.mock { position: absolute; left: 92mm; top: 0; width: 189mm; height: 210mm; display: flex; align-items: center; justify-content: center; }
.fit { transform-origin: 0 0; }   /* boite = taille reduite, le cadre remplit exactement la boite */
.tftnote { position: absolute; left: 92mm; right: 16mm; bottom: 24mm; text-align: center; font-size: 12px; color: #9AA0A8; }
/* page de garde */
.cover .brand { position: absolute; left: 16mm; top: 40mm; }
.cover .brand .logo { font-size: 44px; font-weight: 600; letter-spacing: 0.02em; }
.cover .brand .by { font-size: 12px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; color: #5F6670; margin-top: 6px; }
.cover .brand .tag { font-size: 20px; color: #9AA0A8; margin-top: 28px; }
.cover .meta { position: absolute; left: 16mm; bottom: 24mm; font-size: 12px; color: #5F6670; line-height: 1.6; }
.cover .list { position: absolute; left: 150mm; top: 34mm; width: 130mm; }
.cover .list h2 { font-size: 11px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; color: #5F6670; margin: 0 0 10px; }
.cover .list ol { margin: 0; padding: 0; list-style: none; }
.cover .list li { display: flex; gap: 12px; font-size: 13px; line-height: 1.4; padding: 7px 0; border-top: 1px solid #262A31; }
.cover .list li span:first-child { color: #5F6670; font-size: 11px; font-weight: 500; letter-spacing: 0.08em; width: 22px; flex: none; padding-top: 2px; }
"""


def page_html(e, i, n, feats):
    f = next(x for x in feats if x["n"] == e["feature"])
    png = (OUT / f"{e['id']}.png").as_uri()
    if e.get("tft"):
        box = f"width:{842 * DASH_SCALE:.0f}px;height:{360 * DASH_SCALE:.0f}px"
        mock = (f'<div class="fit" style="{box};transform:scale({DASH_SCALE})"><div class="dash">'
                f'<div class="screen-wrap"><img src="{png}" alt=""></div></div></div>')
        note = '<p class="tftnote">As shown on the bike\'s 10.25" TFT</p>'
    else:
        box = f"width:{414 * PHONE_SCALE:.0f}px;height:{868 * PHONE_SCALE:.0f}px"
        mock = (f'<div class="fit" style="{box};transform:scale({PHONE_SCALE})"><div class="iphone">'
                '<div class="k action"></div><div class="k vol-up"></div><div class="k vol-down"></div><div class="k power"></div>'
                f'<div class="screen-wrap"><div class="island"></div><img src="{png}" alt=""></div></div></div>')
        note = ""
    state = html.escape(e["state"]) if e["state"] else ""
    return f"""
<section class="page">
  <div class="margin">
    <div class="feat">Feature {e['feature']:02d}</div>
    <div class="title">{html.escape(e['title'])}</div>
    {f'<div class="state">{state}</div>' if state else ''}
    <div class="ftitle">{html.escape(f['title'])}</div>
    <div class="file">screens/{html.escape(e['src'])}</div>
  </div>
  <div class="mock">{mock}</div>
  {note}
  <div class="foot"><span>RIDE by BMW Motorrad · Mockups</span><span>{i} / {n}</span></div>
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

        n = len(seq)
        doc = ("<!doctype html><html><head><meta charset='utf-8'>"
               f"<link rel='stylesheet' href='{(ROOT / 'design-system' / 'fonts' / 'inter.css').as_uri()}'>"
               f"<link rel='stylesheet' href='{(ROOT / 'design-system' / 'iphone.css').as_uri()}'>"
               f"<style>{CSS}</style></head><body>"
               + cover_html(seq, feats, n)
               + "".join(page_html(e, i + 1, n, feats) for i, e in enumerate(seq))
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
    print(f"{Path(args.out).relative_to(ROOT) if Path(args.out).is_relative_to(ROOT) else args.out} : {n + 1} pages, {size} Ko")


if __name__ == "__main__":
    main()
