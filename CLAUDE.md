# Hackathon Zurich — Workflow mockups app mobile

Ce repo produit des **mockups d'app mobile en HTML statique**, screenshotés en PNG.
Source de vérité produit : `DESIGN.md`. Source de vérité visuelle : les images dans `refs/`.

## Arborescence

| Dossier | Rôle |
|---|---|
| `refs/` | Screenshots de référence (apps existantes, Figma, inspirations). **Lecture seule.** |
| `screens/` | Un fichier HTML autonome par écran (`home.html`, `onboarding-1.html`, …) |
| `out/` | PNG exportés par Playwright (`out/home.png`) |
| `assets/` | Images générées (illustrations, photos, textures) — jamais de stock externe |
| `design-system/` | `tailwind.js` (vendorisé) + `tokens.md` : palette, typo, composants |
| `scripts/` | Outils : screenshot (`shot.py`), PDF (`export_pdf.py`), captures galerie (`shot_gallery.py`), génération d'image, tuiles, setup Windows |
| `index.html` | Galerie de démo à la racine (GitHub Pages) : 10 features (`screens/features.js`), cadre écran seul (`design-system/iphone.css`) |
| `docs/` | `RIDE-mockups.pdf` (une page par écran et par état) et captures de la galerie |

## Règles de production d'un écran

1. **Un écran = un fichier HTML autonome** dans `screens/`. Pas de build, pas de bundler.
   Styles : `<link rel="stylesheet" href="../design-system/tokens.css">` (tokens de DESIGN.md,
   Inter vendorisée, chrome iOS, composants) + `<script src="data.js">` (données partagées,
   `statusBar()`, `tabBar()`, `homeIndicator()`, `star()`). **Rien ne vient d'un CDN** : si le
   réseau ou un proxy bloque une ressource, la page rend sans style et le PNG est faux sans la
   moindre erreur. Tailwind reste disponible en local (`../design-system/tailwind.js`) mais les
   écrans RIDE n'en ont pas besoin.
   Carte : Leaflet vendorisé (`../design-system/leaflet/`) + tuiles en cache local dans
   `design-system/tiles/<fournisseur>/{z}/{x}/{y}.png`, servies hors-ligne. Le fournisseur est choisi par
   `scripts/cache_tiles.py` et publié dans `design-system/tiles/source.js` (commité, sans clé) :
   MapTiler `dataviz-dark` si la variable d'environnement `MAPTILER_KEY` existe (`setx MAPTILER_KEY "..."`
   puis rouvrir le terminal ; jamais de clé dans un fichier du repo), sinon OSM avec labels gommés par
   Pillow (`tiles/_raw/osm` brut → `tiles/osm` servi) et assombri par le filtre CSS `.map-osm`.
   Dans un écran : `<script src="../design-system/leaflet/leaflet.js">`, puis `../design-system/tiles/source.js`,
   puis `data.js` ; la carte s'obtient avec `rideTileLayer(map)` et se cadre avec `rideFitBounds(map, bounds,
   { paddingTopLeft, paddingBottomRight })` dans un `<div class="map-slot">` (zoom entier + scale CSS + tuiles
   recopiées sur un canvas : aucune couture, aucun flou ; `zoomSnap: 1` obligatoire). Épaisseur visuelle des
   polylines via l'option `vw`, marqueurs et étiquettes en `.keep-size`.
   Après tout changement de zoom ou de zone : `python scripts/cache_tiles.py <ecran>[#etat]`
   (`--reprocess` regénère `tiles/osm` après un changement de l'algorithme de gommage).
2. **Viewport 390 × 844** (iPhone 14/15). Le contenu vit dans un conteneur de cette taille exacte :
   ```html
   <meta name="viewport" content="width=390, initial-scale=1">
   <body class="m-0 bg-neutral-100 flex justify-center">
     <div class="w-[390px] h-[844px] overflow-hidden relative bg-white">…</div>
   </body>
   ```
   Status bar iOS (heure, réseau, batterie) et home indicator inclus, dessinés en HTML/SVG.
3. **Données réalistes, toujours.** Prénoms suisses/français, montants en CHF, dates au format
   `12 sept.`, vrais libellés métier. **Interdits absolus** : lorem ipsum, « Titre ici »,
   `Lorem`, `Placeholder`, `Item 1 / Item 2`, blocs gris `bg-gray-200` qui remplacent une image,
   avatars vides, `<img src="https://via.placeholder.com/...">`.
4. **Aucune image externe non générée.** Trois options seulement :
   - SVG inline (icônes, logos, illustrations simples) ;
   - gradient / forme CSS ;
   - fichier dans `assets/` produit par `scripts/gen_image.py` (voir plus bas), référencé en
     `../assets/nom.png`.
   Les icônes : SVG inline (style Lucide/Heroicons recopié à la main), pas de CDN d'icônes.
5. **Pas de JS applicatif.** C'est un mockup, pas un prototype. Les états (onglet actif, toggle on)
   sont codés en dur dans le HTML. Un écran par état si besoin (`home.html`, `home-empty.html`).

## Boucle obligatoire après chaque écran

```
1. Écrire screens/<nom>.html
2. python scripts/shot.py <nom>            → out/<nom>.png
3. Ouvrir out/<nom>.png ET les refs/ correspondantes, côte à côte
4. Lister EXACTEMENT 3 écarts (les 3 plus visibles), formulés concrètement :
   ✗ "l'espacement est mauvais"
   ✓ "padding horizontal 16px au lieu de 20px dans les refs"
   ✓ "la carte a un border-radius 8px, les refs sont à 16px"
   ✓ "le titre est en 18px semibold, les refs sont en 22px bold"
5. Corriger les 3 écarts dans le HTML
6. python scripts/shot.py <nom>            → PNG final dans out/
```

Ne jamais déclarer un écran terminé sans avoir fait ce cycle au moins une fois.

## Screenshot

```bash
python scripts/shot.py 04-route            # screens/04-route.html → out/04-route.png
python scripts/shot.py "08-explore#heat"   # état #heat de l'écran → out/08-explore-heat.png
python scripts/shot.py 04-route --full-page
python scripts/shot.py --all
```
Un écran peut exposer des états via `location.hash` (`#heat`, `#fun`…) : un PNG par état.
Rend en 390×844, `device_scale_factor=2` (PNG 780×1688, qualité retina). Si l'artboard visible n'est pas
`.screen` mais `.tft` (1920×720 : `10-ride-mode#bike` et les écrans du TFT moto `screens/tft-0N-*.html`), le viewport
suit sa taille (PNG 3840×1440).

```bash
python scripts/export_pdf.py               # re-capture la sélection de features.js (RIDE_SEQUENCE), puis docs/RIDE-mockups.pdf
python scripts/shot_gallery.py             # docs/gallery-*.png (index.html en 1440×900 @2x)
python scripts/export_html.py              # dist/RIDE-maquettes-html/ + .zip : dossier autonome à envoyer (écrans, data, tokens, carte, photos)
```
Contrôle visuel du PDF (poppler absent sous Windows) : `pip install pypdfium2` puis rasteriser les pages avec
`pypdfium2.PdfDocument(...)[i].render(scale=1.6).to_pil()` ; ce n'est pas un prérequis du repo.
Prérequis : `pip install playwright && python -m playwright install chromium`.

Le script **échoue volontairement** si Tailwind n'est pas appliqué, plutôt que de produire
un PNG non stylé. `CHROMIUM_PATH=/chemin/vers/chrome` force un binaire Chromium précis.

## Génération d'images — DeepInfra

Pour toute image qu'on ne peut pas dessiner en SVG/CSS (photo produit, illustration, avatar,
texture de fond) :

```bash
python scripts/gen_image.py "photo of a bowl of granola, top view, soft daylight, white marble" \
    assets/granola.png --size 1024x1024
```

- Clé API lue **uniquement** dans la variable d'environnement `DEEPINFRA_API_KEY`.
  Jamais de clé dans un fichier du repo. `.env` est gitignoré.
  Windows : `setx DEEPINFRA_API_KEY "..."` puis rouvrir le terminal.
- Modèle par défaut : `black-forest-labs/FLUX-1-schnell` (le moins cher, ~0.0005 $/image).
  Autre modèle : `--model black-forest-labs/FLUX-1.1-pro`.
- Options : `--size 1024x1024` (défaut), `--seed 42` (reproductible), `--steps 4`.
- Endpoint : API images OpenAI-compatible de DeepInfra.

Toutes les images du projet sont listées dans `scripts/gen_all_images.py` (une passe, seed fixe,
préfixe de prompt DESIGN.md §5) : `assets/routes/<col>.png` (3:2), `assets/routes/<col>-tall.png`
(9:16), `assets/avatars/<rider>.png`. Une nouvelle image = une ligne dans ce script, pas un appel
à la main.

## Design system

`design-system/tokens.md` tient la palette, l'échelle typographique et les rayons.
`design-system/tailwind.js` est une copie figée du build CDN Tailwind — ne pas l'éditer.
Tout nouvel écran réutilise ces tokens ; on n'invente pas une couleur au cas par cas.
Si un token manque, on l'ajoute dans `tokens.md` d'abord.

## Ne pas toucher

`.claude/settings.json` et `.entire/` (hooks Entire, checkpoints). Ajout uniquement.
