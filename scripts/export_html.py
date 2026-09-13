#!/usr/bin/env python3
"""Assemble un dossier autonome des maquettes HTML, a envoyer a quelqu'un qui veut les ouvrir ou les modifier
sans le repo : ecrans, donnees, tokens, polices, Leaflet et tuiles hors-ligne, photos, galerie, README.

    python scripts/export_html.py                 # dist/RIDE-maquettes-html/ + dist/RIDE-maquettes-html.zip
    python scripts/export_html.py -o C:/chemin    # ailleurs

Tout s'ouvre en double-cliquant (file://), aucun serveur ni build. dist/ est gitignore.
"""
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = "RIDE-maquettes-html"

README = """# RIDE by BMW Motorrad — maquettes HTML

Douze écrans d'app mobile en HTML statique (390 × 844), sans build ni serveur. Tout s'ouvre en double-cliquant.

## Ouvrir

- `index.html` : la galerie (10 features, flèches ← / → entre les écrans).
- `screens/<nom>.html` : un écran seul. Certains écrans ont plusieurs états, ajoutés dans l'URL après `#` :

| Écran | Fichier | États |
|---|---|---|
| Splash | `screens/01-splash.html` | animé, `#connected` |
| Home | `screens/02-home.html` | |
| Destination | `screens/03-destination.html` | |
| Route (slider Fast ↔ Fun) | `screens/04-route.html` | cliquer les crans du slider |
| Route detail | `screens/05-route-detail.html` | |
| Companion (vocal) | `screens/06-voice.html` | animé, `#live`, `#done` |
| Alpine Loop | `screens/07-trip.html` | `#swap` |
| Explore | `screens/08-explore.html` | `#heat` |
| Segment Kesselberg | `screens/09-segment.html` | |
| Ride mode | `screens/10-ride-mode.html` | `#feedback`, `#bike` (écran moto 1920 × 720) |
| Ride complete | `screens/11-recap.html` | |
| Profile | `screens/12-profile.html` | |

## Modifier

- Les textes et chiffres sont dans `screens/data.js` (un seul endroit, partagé par tous les écrans).
- Les couleurs, la typographie et les composants sont dans `design-system/tokens.css` (règles dans `DESIGN.md`).
- Chaque écran est un fichier HTML autonome : son style propre est dans la balise `<style>` en haut, sa construction
  dans le `<script>` en bas. Aucune ressource ne vient d'Internet (police Inter, Leaflet et tuiles de carte sont dans
  `design-system/`, les photos dans `assets/`).
- La liste des 10 features et l'ordre de la galerie sont dans `screens/features.js`.

Ouvrir les fichiers dans n'importe quel éditeur (VS Code, Sublime…), enregistrer, recharger le navigateur.
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default=str(ROOT / "dist"))
    args = ap.parse_args()
    dst = Path(args.out) / NAME
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)

    ignore = shutil.ignore_patterns("_raw", "__pycache__", "tailwind.js", ".gitkeep", "test*.html")
    shutil.copytree(ROOT / "screens", dst / "screens", ignore=ignore)
    shutil.copytree(ROOT / "design-system", dst / "design-system", ignore=ignore)
    shutil.copytree(ROOT / "assets", dst / "assets", ignore=ignore)
    shutil.copy(ROOT / "index.html", dst / "index.html")
    shutil.copy(ROOT / "DESIGN.md", dst / "DESIGN.md")
    (dst / "README.md").write_text(README, encoding="utf-8")

    zip_path = shutil.make_archive(str(dst), "zip", root_dir=dst.parent, base_dir=NAME)
    files = sum(1 for p in dst.rglob("*") if p.is_file())
    size = sum(p.stat().st_size for p in dst.rglob("*") if p.is_file()) // 1024
    print(f"{dst} : {files} fichiers, {size} Ko\n{zip_path} : {Path(zip_path).stat().st_size // 1024} Ko")


if __name__ == "__main__":
    main()
