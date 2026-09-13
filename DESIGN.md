# DESIGN.md : RIDE by BMW Motorrad

Direction : premium, sobre, fond sombre. Référence mentale : l'app Porsche, Apple Maps en mode sombre, le cockpit d'une BMW la nuit. Rien ne crie, mais l'app n'est pas austère : les couleurs sémantiques portent l'information (jauges, étoiles, météo, tags), les vraies photos donnent envie de rouler. La qualité vient de la typographie, des espacements, des vraies photos et de la vraie carte. Toute décision qui n'est pas couverte ici se tranche vers « moins ».

## 1. Palette

**Fond et surfaces** (noirs chauds, jamais bleutés)

- `bg`: #0A0B0D
- `surface-1`: #121417 (cards)
- `surface-2`: #1A1D22 (cards élevées, bottom sheets)
- `border`: #262A31 (1 px, toujours)
- `border-strong`: #343941 (états focus, séparateurs marqués)

**Texte**

- `text-1`: #F4F5F7 (titres, valeurs)
- `text-2`: #9AA0A8 (labels, descriptions)
- `text-3`: #5F6670 (métadonnées, placeholders)

**Accent BMW**

- `accent`: #1C69D4 (bouton primaire, état actif, tab sélectionnée)
- `accent-bright`: #4D8FE6 (texte sur fond sombre, liens, valeurs mises en avant)
- `accent-soft`: rgba(28,105,212,0.14) (fond des chips actives, halo)

**Sémantique** (désaturés), chacune avec son fond teinté `*-soft` à 14 % pour les icônes, tags et alertes

- `positive`: #3FBF7F (bon, connecté, Loved it, scenic)
- `warning`: #D9A441 (avertissements, soleil, communauté)
- `danger`: #D9534F
- `weather`: #6FA8DC (météo, alpin, températures)
- `star`: #E4B75A (or des notes et des étoiles, uniquement pour les notes)

**Route sur la carte**

- `route-selected`: #F4F5F7 (blanc, 4 px, halo rgba(244,245,247,0.25) 10 px, retombée rgba(244,245,247,0.08) 18 px pour que le halo se lise comme un halo et non comme un contour)
- `route-alt`: #4A5058 (2.5 px, opacité 0.6 ; toujours sous le halo du tracé sélectionné)
- `route-day1` / `day2` / `day3` : #F4F5F7, #4D8FE6, #9AA0A8

**Règle d'usage** : un écran contient au maximum un CTA en `accent` plein. Les couleurs sémantiques et `star` servent à l'information : remplissage des jauges (Curviness `accent-bright`, Scenic `positive`, Weather `weather`, Community `warning`), étoiles des notes, icônes sur fond teinté, tags, alertes. Toujours désaturées, jamais sur une surface entière, jamais sur du texte courant.

## 2. Typographie

Une seule famille : **Inter** (Google Fonts, poids 400, 500, 600). Jamais de condensé, jamais de capitales sur les titres.

- `display`: 34 px / 600 / letter-spacing -0.02em (chiffres clés : durée, distance)
- `display-xl`: 56 px / 600 / -0.02em (distance de manœuvre en ride mode uniquement, lisible avec des gants)
- `title-1`: 26 px / 600 / -0.01em (titre d'écran)
- `display-2`: 26 px / 600 / -0.015em (chiffres des cards jour de l'écran trip)
- `title-2`: 20 px / 600 (titre de card, nom de col)
- `body`: 15 px / 400 / line-height 1.45
- `body-strong`: 15 px / 500
- `caption`: 13 px / 400 / text-2
- `label`: 11 px / 500 / letter-spacing 0.08em / capitales / text-3 (uniquement pour les petits labels de section et sous les chiffres)

Chiffres : `font-variant-numeric: tabular-nums` partout.

## 3. Espacements et formes

Grille 4 px. Valeurs autorisées : 4, 8, 12, 16, 20, 24, 32, 40.

- Marge latérale d'écran : 20 px
- Espace entre cards : 12 px
- Padding interne des cards : 16 px
- Rayon cards : 16 px ; boutons : 12 px ; chips : 999 px ; avatars : cercle
- Ombres : aucune. La hiérarchie vient des surfaces et de la bordure 1 px.
- Dégradés : interdits sur les surfaces. Autorisés uniquement en overlay sur les photos (voir §5), qui peuvent recevoir une légère teinte bleue (`rgba(28,105,212,0.10)` mélangée au noir) pour rester dans la même lumière.

## 4. Composants

**Bouton primaire** : hauteur 52 px, fond `accent`, texte `text-1` 15/500, rayon 12, pleine largeur. Un seul par écran.
**Bouton secondaire** : hauteur 52 px, fond `surface-2`, bordure `border`, texte `text-1`.
**Bouton tertiaire** : texte `accent-bright`, sans fond.
**Chips** : hauteur 34 px, padding 0 14 px, fond `surface-2`, bordure `border` ; active : fond `accent-soft`, bordure `accent`, texte `accent-bright` ; choisie (réponse déjà donnée, écran vocal) : bordure `border-strong`, texte `text-1`, sans accent.
**Tag** (caractère d'un segment) : 22 px, padding 0 8 px, 11 px / 500, fond `*-soft`, texte couleur pleine : Twisties → `accent`, Alpine → `weather`, Iconic → `warning`, Lakeside → `positive`.
**Icône sur fond teinté** : 28 à 36 px, rayon 8 à 10, fond `*-soft`, icône Lucide dans la couleur pleine. Sert aux listes (sections, points d'intérêt, préférences, réglages) et aux tuiles de chiffres.
**Card** : `surface-1`, bordure `border`, rayon 16, padding 16.
**Card photo** : image 3:2 en haut, coins supérieurs 16, overlay bas linéaire rgba(10,11,13,0) → rgba(10,11,13,0.85) sur les 55 % inférieurs, titre `title-2` en blanc posé sur l'overlay, métadonnées `caption` en dessous de l'image dans une zone `surface-1`.
**Jauge** : piste `border` 4 px rayon 999, remplissage dans la couleur sémantique de la mesure (voir §1, `text-1` par défaut), valeur en `body-strong` à droite.
**Slider Fast ↔ Fun** : piste `border` 4 px, 3 crans marqués par des points 6 px, poignée 28 px blanche avec bordure 2 px `accent`, labels `caption` sous les crans.
**Bottom sheet** : `surface-2`, coins supérieurs 20, poignée 36×4 px `border-strong` centrée, padding 20.
**Tab bar** : 84 px avec safe area, `surface-1`, bordure haute `border`, 4 onglets, icône 24 px + label 11 px, actif en `text-1`, inactif en `text-3`. Jamais en accent.
**Status bar** : bande vide de 59 px (safe area iPhone 15 Pro), sans heure ni icônes : la maquette ne montre que l'app (demande de Tim, 13 sept. 2026). La hauteur est conservée pour que les écrans gardent leur mise en page.
**Avatar** : 32 ou 40 px, photo générée, bordure 1 px `border`.
**Icônes** : Lucide uniquement, 20 px dans le texte, 24 px dans les boutons et la tab bar, stroke 1.5. Jamais d'emoji, jamais d'icône multicolore : une icône est `text-1` / `text-2`, ou prend la couleur sémantique de son fond teinté.

## 5. Images et carte

**Photos** : générées via `scripts/gen_image.py` (DeepInfra, FLUX). Format 3:2 (1200×800) pour les cards, 9:16 pour les plein écran. Prompt de base à préfixer : « photorealistic editorial photograph, muted cinematic color grading, soft directional light, no text, no logos, no people unless specified, ». Sujets : routes de col alpin (Kesselberg, Sudelfeld, Stelvio, Grimsel...), lacs bavarois, une BMW R 1300 GS garée sur une route de montagne, portraits neutres pour les avatars (buste, fond uni sombre, léger sourire). Toute photo reçoit un filtre CSS : `saturate(0.85) contrast(1.05)`. Aucune image de stock, aucun placeholder, aucune illustration vectorielle de montagne.

**Carte** : Leaflet 1.9 (vendorisé) avec tuiles MapTiler `dataviz-dark` (raster 256 px @2x, clé dans `MAPTILER_KEY`, attribution masquée dans le mockup), assombries (`brightness(0.65)`) pour que le sol reste sous `surface-2`. Sans clé : tuiles OSM avec labels gommés à la mise en cache et filtre `invert(1) hue-rotate(180deg) saturate(0.2) brightness(0.45) contrast(1.25)`. Un voile `bg` → transparent de 64 px sous la status bar quand la carte y passe. Tracés en polylines avec des coordonnées réelles approximatives (Munich 48.137,11.575 ; Starnberg 47.999,11.339 ; Bad Tölz 47.760,11.558 ; Walchensee 47.593,11.328 ; Garmisch 47.492,11.095). Position actuelle : point blanc 12 px avec halo `accent-soft` 28 px. Aucune carte dessinée en SVG.

**Écran TFT moto** (10,25", artboard 1920 × 720, `screens/tft-0N-*.html`) : même palette et mêmes tokens que l'app, typographie ×2,4 (`.tft-label` 24, `.tft-cap` 24, `.tft-body` 30, `.tft-h2` 32, `.tft-title` 44, `.tft-value` 64 / 96, `.tft-dist` 120), marges 96 px latérales et 40 px verticales, aucun texte sous 24 px. Une information principale au centre, la vitesse toujours visible à droite en `accent-bright` quand on roule, limite de vitesse en disque blanc monochrome. Pas de tactile : la molette du Multi-Controller déplace un focus unique (anneau `accent`, `.tft-btn.focus`) et la ligne basse dit ce que fait la pression ou la voix. Photos autorisées uniquement en vignette (avatars). Flèche de manœuvre en `text-1`.

## 6. Mouvement

Transitions d'écran : fade 200 ms. Micro-interactions : 150 à 250 ms, easing `cubic-bezier(0.2, 0, 0, 1)`. Compteurs animés sur les chiffres du slider (300 ms). Orbe vocal : cercle 120 px, blanc à 90 %, avec du volume pour se lire comme un vrai objet lumineux et non comme un disque plat : dégradé radial subtil (blanc en haut à gauche vers gris clair au bord ; ce n'est pas une surface, §3 ne s'applique pas), anneau fin 1 px blanc à 35 %, halo blanc doux de 40 px à 10 %. Pulsation d'échelle 1 → 1.06 quand le compagnon parle, bordure `accent` quand l'utilisateur parle. Jamais de glow coloré, jamais de particules.

## 7. Interdits (à vérifier avant chaque export)

- Orange, dégradés de surface, ombres portées, condensé, capitales sur titres, emojis.
- Plus d'un élément accent plein par écran.
- Plus de 3 blocs d'information sous la ligne de flottaison sur un écran principal.
- Texte sous 11 px, contraste sous 4.5:1.
- Tab bar qui chevauche du contenu (padding-bottom 100 px sur le scroll).
- Lorem ipsum, données incohérentes entre écrans (mêmes chiffres partout : 104 km, 1 h 30 pour Balanced, etc.).
