# Design tokens RIDE

`DESIGN.md` fait foi ; ce fichier résume ce que `tokens.css` expose. Un token manquant s'ajoute ici et dans
`tokens.css` avant d'être utilisé dans un écran. Aucune valeur inventée au cas par cas.

## Couleurs (`tokens.css` `:root`)

| Token | Valeur | Usage |
|---|---|---|
| `--bg` | #0A0B0D | fond d'écran |
| `--surface-1` / `--surface-2` | #121417 / #1A1D22 | cards / cards élevées, bottom sheets, champs |
| `--border` / `--border-strong` | #262A31 / #343941 | bordure 1 px partout / focus, séparateurs marqués |
| `--text-1` / `--text-2` / `--text-3` | #F4F5F7 / #9AA0A8 / #5F6670 | titres et valeurs / labels / métadonnées |
| `--accent` / `--accent-bright` / `--accent-soft` | #1C69D4 / #4D8FE6 / rgba(28,105,212,.14) | CTA unique / texte accent / chips actives |
| `--positive` `--warning` `--danger` `--weather` (+ `*-soft` à 14 %) | #3FBF7F #D9A441 #D9534F #6FA8DC | sémantique désaturée : jauges, icônes teintées, tags, alertes |
| `--star` | #E4B75A | étoiles et notes |
| `--route-selected` `--route-alt` `--route-day1..3` | voir DESIGN.md §1 | tracés Leaflet |

## Typographie (classes)

`.display` 34/600 · `.display-2` 26/600 · `.title-1` 26/600 · `.title-2` 20/600 · `.body` 15/400 · `.body-strong` 15/500 ·
`.caption` 13/400 text-2 · `.label` 11/500 capitales text-3. Inter vendorisée (`fonts/inter.css`), chiffres tabulaires.

## Espacements et formes

Grille 4 px, `--gutter` 20 px, `--r-card` 16, `--r-btn` 12, `--r-sheet` 20, `--r-chip` 999. Aucune ombre, aucun dégradé de surface.

## Composants (`tokens.css`)

`.screen` (390×844) · `.statusbar` / `.home-indicator` / `.tabbar` (`data.js`) · `.btn-primary` `.btn-secondary` `.btn-tertiary` ·
`.chip` (`.active`, `.picked`) · `.tag.{accent,positive,warning,weather}` · `.ico-tint.{…}` · `.stars` · `.card` `.card-photo` + `.overlay` · `.gauge-track` / `.gauge-fill` · `.avatar` · `.sheet` + `.sheet-handle` ·
`.scroll` (padding-bottom 100 px) · `.seg` (ligne segment) · `.list-row` · `.stat` · `.alert` (`.warning`, `.weather`) ·
`.actions-bar` + `.scroll.under-actions` · `.back-btn` · `.tft` (artboard 1920×720 du TFT moto, `.tft-dist` `.tft-street` `.tft-then` `.tft-value` `.tft-label`).

## Carte

Leaflet vendorisé, `.map-slot` + `rideFitBounds()` (`data.js`), `.keep-size` sur marqueurs et étiquettes, fond choisi par `tiles/source.js`.

## Cadres de présentation (hors téléphone)

`iphone.css` : `.iphone` (cadre iPhone 15 Pro : coins 55 px, bezel titane 12 px, Dynamic Island, boutons, ombre douce) et
`.dash` (cadre tableau de bord du TFT 10,25"). Utilisés par `index.html` et `scripts/export_pdf.py`, jamais dans un écran.
