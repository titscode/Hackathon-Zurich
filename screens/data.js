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

  /* Alpine Loop, 3 jours */
  trip: {
    name: "Alpine Loop",
    days: [
      { n: 1, from: "Munich", to: "Innsbruck", km: "215 km", time: "4 h 10",
        passes: ["Kesselberg", "Achenpass"], weather: "Sunny, 19 °C", stay: "Hotel Innsbruck" },
      { n: 2, from: "Innsbruck", to: "Bormio", km: "245 km", time: "5 h 30",
        passes: ["Timmelsjoch", "Stelvio"], weather: "6 °C at the top · side wind", stay: "Bormio" },
      { n: 3, from: "Bormio", to: "Munich", km: "310 km", time: "5 h 50",
        passes: ["Livigno", "Ofenpass"], weather: "Clear", stay: "Home" },
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

/* Étoile pleine pour les notes. */
function star(size) {
  return `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></svg>`;
}
