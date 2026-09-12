# SCREENS.md : RIDE by BMW Motorrad, brief des écrans

Contexte : prototype de hackathon, mockups mobiles 390×844 en HTML statique autonome (un fichier par écran dans `screens/`), reliés par des liens. Textes UI en anglais, courts. Données simulées cohérentes d'un écran à l'autre. Pas de backend. Style : `DESIGN.md` fait foi.

## Données partagées (à mettre dans `screens/data.js`, importé par tous les écrans)

**Utilisateur** : Tim, Munich, BMW R 1300 GS connectée, carburant 78 %, autonomie 312 km, dernier ride il y a 2 jours. Météo Munich : 18 °C, sunny, light NW wind, « Clear until 15:00 ».

**Trajet Munich → Garmisch-Partenkirchen** :

- **Fastest** : A95, 1 h 05, 90 km, curviness 2/10, scenic 4/10, 0 community segments.
- **Balanced** : Starnberger See, Murnau, Oberau, 1 h 30, 104 km, curviness 5/10, scenic 7/10, 1 segment (Kochelsee Uferstraße).
- **Most fun** : Bad Tölz, Sylvensteinspeicher, Walchensee, Kesselberg, 2 h 20, 148 km, curviness 9/10, scenic 9/10, 3 segments (Kesselberg, Kochelsee Uferstraße, Achenpass). Alerte : « Light rain likely near Kesselberg after 15:00. Leave before 12:30. »

**Segments communautaires Bavière (8)** : Kesselberg (Marco_K, 4.9, 3 210 rides, 4.2 km, curv 9, twisties iconic alpine) ; Sudelfeld (AlpineAnna, 4.7, 2 140, 16 km, curv 8) ; Tatzelwurm (Flo_R18, 4.6, 1 880, 9 km, curv 7) ; Deutsche Alpenstraße Tegernsee → Schliersee (LisaGS, 4.5, 1 420, 22 km, curv 5, lakeside) ; Achenpass (Flo_R18, 4.4, 1 260, 18 km, curv 6) ; Roßfeld Panoramastraße (JonasB, 4.8, 980, 16 km, curv 8, alpine iconic) ; Oberjoch (MaxRT, 4.3, 760, 12 km, curv 7) ; Kochelsee Uferstraße (Marco_K, 4.2, 640, 7 km, curv 4, lakeside).

**Dream rides** : Stelvio North Face (48 hairpins), Grimsel Pass, Susten Pass, Passo Gardena, Timmelsjoch, Großglockner.

**Alpine Loop (3 jours)** : Day 1 Munich → Innsbruck via Kesselberg, Achenpass, 215 km, 4 h 10, hôtel Innsbruck ; Day 2 Innsbruck → Bormio via Timmelsjoch (6 °C au sommet), Stelvio (side wind), 245 km, 5 h 30 ; Day 3 Bormio → Munich via Livigno, Ofenpass, 310 km, 5 h 50.

**Préférences apprises** : tight corners, avoids highways, early starts, coffee stops with a lake view, accepts 20 % detour, no gravel.

## Écrans (fichier, contenu, lien sortant)

**01-splash.html** : logo RIDE en Inter 600 34 px, « Find your best road », tracé blanc qui se dessine sur fond `bg`, puis « Connecting to your R 1300 GS » avec check `positive`. Lien auto vers 02 après 2 s.

**02-home.html** : « Ready to ride, Tim? » (`title-1`), ligne météo compacte en `caption`, pastille « R 1300 GS · 78 % · 312 km ». Deux cards photo empilées, hauteur 168 px chacune : « Go somewhere » (photo route de campagne bavaroise au petit matin) et « Plan a trip » (photo col alpin). Titre `title-2` sur overlay, sous-titre `caption`. Puis section `label` « Near you this weekend » avec 2 cards photo horizontales (Kesselberg, Sudelfeld) 160×200. Tab bar. Liens : 03, 06, 08, 12.

**03-destination.html** : champ « Where to? » `surface-2`, 3 récents (Garmisch-Partenkirchen, Salzburg, Innsbruck) en liste, bouton secondaire « Take me out of the city ». Lien : Garmisch → 04.

**04-route.html** (écran signature) : carte Leaflet réelle sur 58 % de la hauteur, tracé Balanced en blanc, alternatives en `route-alt`, position actuelle. Bottom sheet : slider Fast ↔ Fun (cran Balanced actif), `display` « 1 h 30 » et « 104 km » côte à côte avec labels dessous, `caption` « +25 min vs fastest · lake views », 4 jauges (Curviness 5/10, Scenic 7/10, Weather Clear, Community 4.1), card segment Kochelsee Uferstraße avec avatar, bouton primaire « Start ride ». Le slider change tracé et chiffres (3 états codés en JS, fade 200 ms). Liens : 05, 10.

**05-route-detail.html** : profil d'altitude en SVG ligne blanche 1.5 px sur fond `surface-1`, liste des segments (Highway, Valley road, Mountain pass) avec durée, points iconiques (Walchensee viewpoint, Café am See, Aral Kochel), alerte gravel en `warning`, météo heure par heure en ligne horizontale. Boutons « Save to my rides » (secondaire) et « Start ride » (primaire).

**06-voice.html** : plein écran `bg`, orbe 120 px centré haut, transcription qui se construit (effet de frappe, pauses 600 ms) avec les 7 répliques du dialogue, chips de réponse rapide sous chaque question du compagnon, ligne « Learning from you: avoids highways · early starts », bouton tertiaire « Replay ». À la fin, lien vers 07 avec « See your Alpine Loop » en primaire.

**07-trip.html** : « Alpine Loop » `title-1`, carte Leaflet avec 3 tracés (day1 blanc, day2 `accent-bright`, day3 `text-2`), slider Fast ↔ Fun compact, 3 cards jour : titre « Day 1 · Munich → Innsbruck », chiffres km et heures en `display` réduit (26 px), cols en chips, météo `caption`, hébergement `caption`, segments inclus avec avatars, bouton tertiaire « Swap » par segment (ouvre une bottom sheet avec 2 alternatives). Boutons « Save trip » (secondaire) et « Send to bike » (primaire).

**08-explore.html** : « Explore » `title-1`, tabs Segments / Riders, bouton secondaire compact « Heat map », chips de filtre (Near me actif, Top rated, Twisties, Alpine, Iconic, This weekend). Fil de cards photo pleine largeur (Kesselberg, Sudelfeld, Tatzelwurm, Roßfeld...) avec photo 3:2, titre sur overlay, ligne avatar + auteur + rides, ligne km + curv + note, bouton tertiaire « Add to route ». Section « Dream rides » : 3 cards photo horizontales. Heat map : même carte Leaflet avec polylines en `accent-bright` d'opacité proportionnelle. Lien : 09.

**09-segment.html** : Kesselberg par Marco_K. Photo 9:16 sur le tiers supérieur avec overlay, titre, note 4.9 et distribution en 5 jauges, description personnelle 3 lignes, profil d'altitude, « Best time: May to October, weekdays before 10:00 », 2 avertissements communauté (gravel after rain, weekend traffic), 3 commentaires avec avatars. Bloc mis en valeur en `surface-2` : « Rated by 3 210 riders. Not an AI guess. » Boutons « Follow segment » (secondaire) et « Add to next trip » (primaire).

**10-ride-mode.html** : fond `bg`, flèche de manœuvre Lucide 96 px en `text-1`, « 400 m » en `display`, « Turn right onto Kesselbergstraße » en `title-2`, ligne basse : 62 km/h, 14 °C in 20 min, 312 km range. Rien en accent sauf rien. Toggle « Bike display » en haut à droite qui affiche la version paysage dans un cadre TFT 10,25". Après 3 s, card feedback « How was Kesselberg? » avec deux boutons secondaires larges (thumbs up, thumbs down) et `caption` « Say "loved it" or "skip" ». Lien : 11.

**11-recap.html** : « Ride complete » `label`, card photo (photo route Kesselberg) avec tracé blanc en overlay et « Munich → Garmisch » `title-2`, grille 3×2 de stats (148 km, 2 h 34, 3 passes, 8.6 avg curviness, 858 m max altitude, 0 motorway km), liste « Segments you rated » (Kesselberg Loved it, Kochelsee Loved it, Achenpass Good) en `positive`, ligne « Your companion learned: you loved Kesselberg, avoided the A95 », bouton primaire « Share this ride ».

**12-profile.html** : avatar 72 px, « Tim », « BMW R 1300 GS », 3 chiffres (42 rides, 6 830 km, 11 passes), badges en chips (Bavarian Explorer, Early Bird, Twisty Hunter), section « What your companion knows » avec les 6 préférences en liste et icône edit, section « Your bike » (78 %, 312 km, tyres OK, last ride 2 days ago), réglages (Units, Language, Companion voice).

**index.html** : panneau de démo hors téléphone, fond `bg`, colonne gauche 320 px : logo, titre, 10 features numérotées en cards `surface-1` (label + caption), chacune ouvrant l'écran cible dans l'iframe 390×844 à droite, cadre smartphone en `surface-2` avec bordure `border-strong` et rayon 44.

## Ordre de construction

1. `data.js` et `tokens.css`.
2. Génération des images (liste complète d'abord, en une seule passe) : 10 routes/cols en 3:2, 2 photos 9:16 (Kesselberg, col alpin pour Plan a trip), 8 avatars.
3. Écrans 02, 04, 08, 06, 07, puis 09, 05, 10, 11, 12, 03, 01, index.
4. Pour chaque écran : screenshot Playwright 390×844 @2x dans `out/`, comparaison avec `refs/`, 3 écarts listés, correction, re-screenshot.
