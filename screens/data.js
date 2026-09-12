/* RIDE by BMW Motorrad — données partagées (SCREENS.md §Données partagées).
   Un seul endroit pour les chiffres : ils doivent être identiques d'un écran à l'autre. */

const RIDE = {
  user: {
    name: "Tim",
    city: "Munich",
    bike: "R 1300 GS",
    bikeFull: "BMW R 1300 GS",
    fuel: 78,
    range: 312,
    lastRide: "2 days ago",
    avatar: "../assets/avatars/tim.png",
    stats: { rides: 42, km: "6 830", passes: 11 },
    badges: ["Bavarian Explorer", "Early Bird", "Twisty Hunter"],
    prefs: [
      "Tight corners",
      "Avoids highways",
      "Early starts",
      "Coffee stops with a lake view",
      "Accepts 20 % detour",
      "No gravel",
    ],
  },

  weather: { temp: "18°", cond: "Sunny", wind: "Light NW wind", note: "Clear until 15:00" },

  /* Munich → Garmisch-Partenkirchen, 3 états du slider Fast ↔ Fun */
  routes: [
    {
      key: "fastest", label: "Fast",
      time: "1 h 05", km: "90 km",
      via: "A95",
      delta: "Fastest route · motorway",
      curviness: 2, scenic: 4, weather: "Clear", community: null,
      segments: [],
      path: [
        [48.137, 11.575], [48.060, 11.520], [47.940, 11.400], [47.800, 11.300],
        [47.660, 11.200], [47.560, 11.130], [47.492, 11.095],
      ],
    },
    {
      key: "balanced", label: "Balanced",
      time: "1 h 30", km: "104 km",
      via: "Starnberger See · Murnau · Oberau",
      delta: "+25 min vs fastest · lake views",
      curviness: 5, scenic: 7, weather: "Clear", community: "4.1",
      segments: ["Kochelsee Uferstraße"],
      path: [
        [48.137, 11.575], [48.060, 11.480], [47.999, 11.339], [47.900, 11.290],
        [47.810, 11.230], [47.680, 11.200], [47.600, 11.180], [47.540, 11.130],
        [47.492, 11.095],
      ],
    },
    {
      key: "fun", label: "Fun",
      time: "2 h 20", km: "148 km",
      via: "Bad Tölz · Sylvensteinspeicher · Walchensee · Kesselberg",
      delta: "+1 h 15 vs fastest · 3 community segments",
      curviness: 9, scenic: 9, weather: "Rain after 15:00", community: "4.7",
      segments: ["Kesselberg", "Kochelsee Uferstraße", "Achenpass"],
      alert: "Light rain likely near Kesselberg after 15:00. Leave before 12:30.",
      path: [
        [48.137, 11.575], [48.020, 11.600], [47.880, 11.590], [47.760, 11.558],
        [47.640, 11.480], [47.580, 11.420], [47.593, 11.328], [47.640, 11.310],
        [47.600, 11.230], [47.540, 11.150], [47.492, 11.095],
      ],
    },
  ],

  /* 8 segments communautaires de Bavière */
  segments: [
    { name: "Kesselberg", path: [[47.618, 11.332], [47.632, 11.338], [47.648, 11.352], [47.662, 11.356]], author: "Marco_K", avatar: "marco-k", rating: 4.9, rides: "3 210",
      km: "4.2 km", curv: 9, tags: ["Twisties", "Iconic", "Alpine"], photo: "kesselberg" },
    { name: "Sudelfeld", path: [[47.672, 12.030], [47.690, 12.052], [47.705, 12.078], [47.716, 12.095]], author: "AlpineAnna", avatar: "alpine-anna", rating: 4.7, rides: "2 140",
      km: "16 km", curv: 8, tags: ["Twisties", "Alpine"], photo: "sudelfeld" },
    { name: "Tatzelwurm", path: [[47.720, 12.104], [47.735, 12.088], [47.748, 12.066]], author: "Flo_R18", avatar: "flo-r18", rating: 4.6, rides: "1 880",
      km: "9 km", curv: 7, tags: ["Twisties"], photo: "tatzelwurm" },
    { name: "Deutsche Alpenstraße", path: [[47.700, 11.745], [47.712, 11.790], [47.718, 11.835], [47.722, 11.862]], sub: "Tegernsee → Schliersee", author: "LisaGS", avatar: "lisa-gs",
      rating: 4.5, rides: "1 420", km: "22 km", curv: 5, tags: ["Lakeside"], photo: "alpenstrasse" },
    { name: "Achenpass", path: [[47.548, 11.632], [47.568, 11.615], [47.590, 11.602], [47.606, 11.598]], author: "Flo_R18", avatar: "flo-r18", rating: 4.4, rides: "1 260",
      km: "18 km", curv: 6, tags: ["Alpine"], photo: "achenpass" },
    { name: "Roßfeld Panoramastraße", path: [[47.628, 13.045], [47.642, 13.062], [47.658, 13.078], [47.672, 13.086]], author: "JonasB", avatar: "jonas-b", rating: 4.8, rides: "980",
      km: "16 km", curv: 8, tags: ["Alpine", "Iconic"], photo: "rossfeld" },
    { name: "Oberjoch", path: [[47.506, 10.418], [47.518, 10.436], [47.530, 10.452]], author: "MaxRT", avatar: "max-rt", rating: 4.3, rides: "760",
      km: "12 km", curv: 7, tags: ["Twisties"], photo: "oberjoch" },
    { name: "Kochelsee Uferstraße", path: [[47.628, 11.348], [47.648, 11.352], [47.668, 11.358], [47.684, 11.362]], author: "Marco_K", avatar: "marco-k", rating: 4.2, rides: "640",
      km: "7 km", curv: 4, tags: ["Lakeside"], photo: "kochelsee" },
  ],

  dreamRides: [
    { name: "Stelvio North Face", sub: "48 hairpins", photo: "stelvio" },
    { name: "Grimsel Pass", sub: "Switzerland", photo: "grimsel" },
    { name: "Susten Pass", sub: "Switzerland", photo: "susten" },
  ],


  /* Heat map (écran 08) : corridors de sorties les plus roulés depuis Munich, poids = rides/12 mois */
  heat: [
    { rides: 3210, path: [[48.137,11.575],[48.020,11.520],[47.900,11.420],[47.760,11.360],[47.660,11.356],[47.618,11.332],[47.560,11.300],[47.492,11.095]] },   // Kesselberg / Walchensee / Garmisch
    { rides: 2140, path: [[48.137,11.575],[48.000,11.700],[47.850,11.780],[47.730,11.900],[47.690,12.052],[47.716,12.095],[47.748,12.066]] },                 // Tegernsee / Sudelfeld / Tatzelwurm
    { rides: 1420, path: [[48.137,11.575],[47.960,11.640],[47.790,11.720],[47.700,11.745],[47.722,11.862],[47.700,11.950]] },                                 // Alpenstraße Tegernsee → Schliersee
    { rides: 1260, path: [[48.137,11.575],[47.950,11.580],[47.760,11.558],[47.640,11.570],[47.548,11.632],[47.606,11.598],[47.470,11.700]] },                 // Bad Tölz / Achenpass / Achensee
    { rides:  980, path: [[48.137,11.575],[48.000,12.100],[47.870,12.600],[47.720,12.900],[47.628,13.045],[47.672,13.086]] },                                 // Chiemsee / Berchtesgaden / Roßfeld
    { rides:  760, path: [[48.137,11.575],[47.950,11.200],[47.800,10.900],[47.620,10.700],[47.506,10.418],[47.530,10.452]] },                                 // Füssen / Oberjoch
    { rides:  640, path: [[47.760,11.558],[47.700,11.450],[47.684,11.362],[47.628,11.348],[47.593,11.328]] },                                                 // Kochelsee Uferstraße / Walchensee
    { rides:  520, path: [[47.492,11.095],[47.400,11.150],[47.300,11.300],[47.270,11.400]] },                                                                 // Garmisch → Innsbruck (Zirler Berg)
  ],

  /* Segments alpins du trip (hors Bavière) : pas dans `segments` pour ne pas changer le fil de 08. */
  tripSegments: [
    { name: "Timmelsjoch",  author: "AlpineAnna", avatar: "alpine-anna", rating: 4.8, rides: "1 120", km: "31 km", curv: 9, note: "6 °C at the top" },
    { name: "Stelvio",      author: "JonasB",     avatar: "jonas-b",     rating: 4.9, rides: "2 650", km: "24 km", curv: 9, note: "48 hairpins · side wind today" },
    { name: "Livigno",      author: "LisaGS",     avatar: "lisa-gs",     rating: 4.5, rides: "540",   km: "38 km", curv: 7, note: "Café at Lago di Livigno" },
    { name: "Ofenpass",     author: "Stefan_W",   avatar: "stefan-w",    rating: 4.4, rides: "720",   km: "22 km", curv: 7, note: "Paved all the way" },
    /* alternatives proposées par le Swap */
    { name: "Umbrail Pass", author: "Stefan_W",   avatar: "stefan-w",    rating: 4.6, rides: "890",   km: "13 km", curv: 9, note: "Sheltered from the wind" },
    { name: "Gavia Pass",   author: "JonasB",     avatar: "jonas-b",     rating: 4.7, rides: "1 050", km: "25 km", curv: 8, note: "Single lane near the top" },
    { name: "Jaufenpass",   author: "Flo_R18",    avatar: "flo-r18",     rating: 4.6, rides: "1 340", km: "19 km", curv: 8, note: "Wide, fast sweepers" },
    { name: "Reschenpass",  author: "MaxRT",      avatar: "max-rt",      rating: 4.1, rides: "2 210", km: "26 km", curv: 4, note: "Lakeside, easy" },
    { name: "Bernina Pass", author: "AlpineAnna", avatar: "alpine-anna", rating: 4.8, rides: "1 720", km: "34 km", curv: 7, note: "Glacier views" },
    { name: "Flüela Pass",  author: "LisaGS",     avatar: "lisa-gs",     rating: 4.6, rides: "980",   km: "27 km", curv: 7, note: "Quiet on weekdays" },
  ],

  /* Alpine Loop, 3 jours (écrans 06 et 07). Chiffres : 215 + 245 + 310 = 770 km, 4 h 10 + 5 h 30 + 5 h 50 = 15 h 30. */
  trip: {
    name: "Alpine Loop", totalKm: "770 km", totalTime: "15 h 30", nights: 2, mode: 2 /* slider : Fun */,
    days: [
      { n: 1, from: "Munich", to: "Innsbruck", km: "215 km", time: "4 h 10", start: "7:00",
        passes: ["Kesselberg", "Achenpass"], weather: "Sunny, 19 °C", stay: "Hotel Innsbruck · 1 night", color: "--route-day1",
        segments: ["Kesselberg", "Achenpass"],
        alts: { "Kesselberg": [["Sudelfeld", "+35 min"], ["Tatzelwurm", "+40 min"]],
                "Achenpass":  [["Deutsche Alpenstraße", "+25 min"], ["Kochelsee Uferstraße", "−10 min"]] },
        /* Munich → Bad Tölz → Kochel → Kesselberg → Walchensee → Sylvenstein → Achenpass → Achensee → Innsbruck */
        path: [[48.137,11.575],[48.020,11.560],[47.900,11.540],[47.760,11.558],[47.700,11.470],[47.660,11.365],
               [47.630,11.335],[47.593,11.328],[47.520,11.290],[47.550,11.440],[47.560,11.530],[47.548,11.632],
               [47.500,11.700],[47.425,11.750],[47.393,11.775],[47.330,11.600],[47.269,11.404]] },
      { n: 2, from: "Innsbruck", to: "Bormio", km: "245 km", time: "5 h 30", start: "7:30",
        passes: ["Timmelsjoch", "Stelvio"], weather: "6 °C at the top · side wind on Stelvio", stay: "Bormio · Hotel Posta", color: "--route-day2",
        segments: ["Timmelsjoch", "Stelvio"],
        alts: { "Timmelsjoch": [["Jaufenpass", "−20 min"], ["Reschenpass", "−45 min"]],
                "Stelvio":     [["Umbrail Pass", "+5 min"], ["Gavia Pass", "+40 min"]] },
        /* Innsbruck → Ötztal → Sölden → Timmelsjoch → Meran → Prad → Stelvio → Bormio */
        path: [[47.269,11.404],[47.250,11.150],[47.230,10.860],[47.100,10.930],[46.970,11.000],[46.905,11.095],
               [46.830,11.170],[46.810,11.240],[46.670,11.160],[46.650,11.000],[46.630,10.770],[46.620,10.590],
               [46.560,10.510],[46.528,10.453],[46.468,10.370]] },
      { n: 3, from: "Bormio", to: "Munich", km: "310 km", time: "5 h 50", start: "7:00",
        passes: ["Livigno", "Ofenpass"], weather: "Clear, 21 °C in Bormio", stay: "Home", color: "--route-day3",
        segments: ["Livigno", "Ofenpass"],
        alts: { "Livigno":  [["Bernina Pass", "+30 min"], ["Umbrail Pass", "+10 min"]],
                "Ofenpass": [["Reschenpass", "+15 min"], ["Flüela Pass", "+45 min"]] },
        /* Bormio → Livigno → Ofenpass → Reschenpass → Landeck → Fernpass → Garmisch → Munich (côté ouest, distinct du jour 1) */
        path: [[46.468,10.370],[46.490,10.210],[46.538,10.135],[46.620,10.200],[46.640,10.290],[46.630,10.440],
               [46.670,10.550],[46.840,10.510],[46.950,10.550],[47.140,10.570],[47.240,10.740],[47.360,10.830],
               [47.400,10.880],[47.492,11.095],[47.700,11.300],[47.900,11.450],[48.137,11.575]] },
    ],
  },

  /* Dialogue vocal (écran 06) : 7 répliques, compagnon (c) / Tim (t). Chips = réponses rapides sous chaque question. */
  voice: {
    learning: "avoids highways · early starts",
    turns: [
      { who: "c", text: "Three days off next week. Where do you want to ride?",
        chips: ["The Alps", "Dolomites", "Surprise me"], pick: "The Alps" },
      { who: "t", text: "The Alps. Passes, the tighter the better." },
      { who: "c", text: "Munich, Innsbruck, Bormio and back. Timmelsjoch and Stelvio on day two: 6 °C at the top, side wind on Stelvio. Still in?",
        chips: ["Still in", "Skip Stelvio", "Shorter day 2"], pick: "Still in" },
      { who: "t", text: "Still in. Early start, I'll pack the liner." },
      { who: "c", text: "Day three is the long one, 310 km back via Livigno and Ofenpass. Coffee at Lago di Livigno on the way?",
        chips: ["Yes, lake view", "Skip the stop", "Make it lunch"], pick: "Yes, lake view" },
      { who: "t", text: "Yes, lake view. And no gravel on the Ofenpass side." },
      { who: "c", text: "Done. Alpine Loop: 770 km, 15 h 30 of riding, no motorway, no gravel. Two hotel nights, Innsbruck and Bormio." },
    ],
  },

  /* Récap de sortie (écran 11) */
  recap: { km: "148 km", time: "2 h 34", passes: "3", curv: "8.6", alt: "858 m", motorway: "0 km" },
};

/* Chrome iOS partagé — DESIGN.md §4. Injecté par chaque écran. */
function statusBar() {
  return `<div class="statusbar">
    <span>09:41</span>
    <span class="icons">
      <svg width="17" height="11" viewBox="0 0 17 11" fill="currentColor" aria-hidden="true">
        <rect x="0" y="7.5" width="3" height="3.5" rx="1"/><rect x="4.6" y="5" width="3" height="6" rx="1"/>
        <rect x="9.2" y="2.5" width="3" height="8.5" rx="1"/><rect x="13.8" y="0" width="3" height="11" rx="1"/>
      </svg>
      <svg width="16" height="11" viewBox="0 0 16 12" fill="currentColor" aria-hidden="true">
        <path d="M8 1.6c2 0 3.9.7 5.4 2l1.1-1.3A10.2 10.2 0 0 0 8 0C5.1 0 2.5 1.1.5 2.9L1.7 4A8.6 8.6 0 0 1 8 1.6z"/>
        <path d="M8 5.6c1 0 1.9.3 2.6.9l1.1-1.3A6.2 6.2 0 0 0 8 4a6.2 6.2 0 0 0-3.7 1.2l1.1 1.3c.7-.6 1.6-.9 2.6-.9z"/>
        <circle cx="8" cy="10" r="1.6"/>
      </svg>
      <svg width="25" height="12" viewBox="0 0 25 12" fill="none" aria-hidden="true">
        <rect x="0.5" y="0.5" width="21" height="11" rx="3" stroke="currentColor" opacity=".45"/>
        <rect x="2" y="2" width="16.4" height="8" rx="1.6" fill="currentColor"/>
        <path d="M23 4v4a2.5 2.5 0 0 0 0-4z" fill="currentColor" opacity=".45"/>
      </svg>
    </span>
  </div>`;
}

function homeIndicator() {
  return `<div class="home-indicator"><i></i></div>`;
}

/* Tab bar — DESIGN.md §4 : actif en text-1, jamais en accent. */
function tabBar(active) {
  const tabs = [
    { key: "ride",    label: "Ride",    href: "03-destination.html",
      d: "M12 2 4.5 20.3 12 17l7.5 3.3z" },
    { key: "explore", label: "Explore", href: "08-explore.html",
      d: "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zm3.5 5.5-2.1 5-5 2.1 2.1-5z" },
    { key: "voice",   label: "Companion", href: "06-voice.html",
      d: "M12 3a3 3 0 0 1 3 3v5a3 3 0 0 1-6 0V6a3 3 0 0 1 3-3zM6 11a6 6 0 0 0 12 0M12 17v4" },
    { key: "profile", label: "Profile", href: "12-profile.html",
      d: "M12 3a4 4 0 1 1 0 8 4 4 0 0 1 0-8zM4 21a8 8 0 0 1 16 0" },
  ];
  return `<nav class="tabbar">${tabs.map(t => `
    <a href="${t.href}" class="${t.key === active ? "active" : ""}">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
           stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="${t.d}"/></svg>
      <span>${t.label}</span>
    </a>`).join("")}</nav>`;
}

/* Segment par nom : les 8 de Bavière d'abord, puis les segments alpins du trip. */
function segByName(name) {
  return RIDE.segments.find(s => s.name === name) || RIDE.tripSegments.find(s => s.name === name);
}

/* Fond de carte partagé — DESIGN.md §5. Le fournisseur vient de design-system/tiles/source.js,
   écrit par scripts/cache_tiles.py (MapTiler dataviz-dark si MAPTILER_KEY, sinon OSM gommé).
   Sans source.js (clone frais) : OSM. Le filtre CSS .map-osm (tokens.css) ne s'applique qu'à OSM.
   `L` n'est touché qu'à l'appel : data.js reste chargeable sans Leaflet. */
function rideTileLayer(map) {
  const t = window.TILES || { provider: "osm", url: "../design-system/tiles/osm/{z}/{x}/{y}.png",
                              tileSize: 256, zoomOffset: 0, maxZoom: 19, dark: false };
  map.getContainer().classList.add(t.dark ? "map-dark" : "map-osm");
  map._rideTiles = L.tileLayer(t.url, { tileSize: t.tileSize, zoomOffset: t.zoomOffset, maxZoom: t.maxZoom }).addTo(map);
  return map._rideTiles;
}

/* Recopie les tuiles chargées dans un seul canvas (positions entières, aucune interpolation) puis masque
   les <img>. Chrome re-rasterise chaque tuile à part dès que le conteneur est mis à l'échelle et laisse
   une couture de 1 px entre elles ; un canvas unique n'a pas de bord interne. Le canvas vit dans le
   tilePane : le filtre CSS .map-osm / .map-dark et l'ordre des couches restent les mêmes. */
function rideFlattenTiles(map) {
  const tiles = map._rideTiles;
  if (!tiles) return;
  const draw = () => {
    const origin = map.getPixelOrigin(), size = tiles.getTileSize(), z = map.getZoom();
    const list = Object.values(tiles._tiles).filter(t => t.current && t.loaded && t.coords.z === z && t.el.naturalWidth)
      .map(t => ({ el: t.el, p: t.coords.scaleBy(size).subtract(origin) }));
    if (!list.length) return;
    const minX = Math.min(...list.map(o => o.p.x)), minY = Math.min(...list.map(o => o.p.y));
    const maxX = Math.max(...list.map(o => o.p.x + size.x)), maxY = Math.max(...list.map(o => o.p.y + size.y));
    const dpr = 2;                                              // tuiles @2x : 512 px pour 256 px CSS
    let cv = map._rideCanvas;
    if (!cv) { cv = map._rideCanvas = document.createElement("canvas"); cv.className = "ride-tiles"; map.getPane("tilePane").appendChild(cv); }
    cv.width = (maxX - minX) * dpr; cv.height = (maxY - minY) * dpr;
    cv.style.width = (maxX - minX) + "px"; cv.style.height = (maxY - minY) + "px";
    L.DomUtil.setPosition(cv, L.point(minX, minY));
    const ctx = cv.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    list.forEach(o => ctx.drawImage(o.el, o.p.x - minX, o.p.y - minY, size.x, size.y));
    tiles.getContainer().style.visibility = "hidden";
  };
  if (tiles.isLoading()) tiles.once("load", draw); else draw();
}

/* Cadrage à zoom fractionnaire sans couture. Chrome laisse une ligne claire de 1 px entre les tuiles
   dès que Leaflet les met à l'échelle (zoom non entier). Ici Leaflet reste à zoom entier (tuiles 512 px
   rendues 1:1 en @2x) dans un conteneur agrandi, réduit ensuite par CSS scale(s), s ∈ ]0.5, 1] :
   le rendu est sur-échantillonné, jamais flou. Le slot (parent du conteneur, .map-slot, overflow hidden)
   définit la zone visible ; les paddings sont en px visibles. Les polylines qui portent `vw` (épaisseur
   visuelle) sont recalées ; les éléments .keep-size (marqueurs, étiquettes) gardent leur taille. */
function rideFitBounds(map, bounds, { paddingTopLeft: [pl, pt] = [0, 0], paddingBottomRight: [pr, pb] = [0, 0] } = {}) {
  const el = map.getContainer(), slot = el.parentElement;
  const W = slot.clientWidth, H = slot.clientHeight;
  Object.assign(el.style, { width: W + "px", height: H + "px", transform: "", transformOrigin: "0 0" });
  if (!map._loaded) map.setView(bounds.getCenter(), 0, { animate: false });   // sinon invalidateSize() est ignoré et la taille reste en cache
  map.invalidateSize({ animate: false });
  const snap = map.options.zoomSnap;
  map.options.zoomSnap = 0;                                   // zoom continu pour la zone utile
  const zf = map.getBoundsZoom(bounds, false, L.point(pl + pr, pt + pb));
  map.options.zoomSnap = snap;
  const zi = Math.ceil(zf - 1e-6), s = Math.pow(2, zf - zi);
  Object.assign(el.style, { width: W / s + "px", height: H / s + "px", transform: `scale(${s})` });
  el.style.setProperty("--s", s);
  map._rideScale = s;
  map.invalidateSize({ animate: false });
  const off = L.point(pr - pl, pb - pt).divideBy(2 * s);
  const sw = map.project(bounds.getSouthWest(), zi), ne = map.project(bounds.getNorthEast(), zi);
  map.setView(map.unproject(sw.add(ne).divideBy(2).add(off), zi), zi, { animate: false });
  map.eachLayer(l => { if (l.setStyle && l.options.vw) l.setStyle({ weight: l.options.vw / s }); });
  rideFlattenTiles(map);
  return s;
}

/* Étoile pleine pour les notes. */
function star(size) {
  return `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></svg>`;
}
