/* RIDE by BMW Motorrad — les 10 features de la démo et la séquence des écrans (SCREENS.md §10 features).
   Source unique pour index.html (galerie) et scripts/export_pdf.py (PDF). Aucune dépendance. */

/* Chaque entrée : id (nom de PNG dans out/), src (ce que la galerie charge : l'animation quand elle existe),
   title, state (lisible), feature (numéro), tft (artboard 1920×720 dans le cadre tableau de bord). */
const RIDE_SEQUENCE = [
  { id: "01-splash-connected",  src: "01-splash.html",           title: "Splash",        state: "Connected to the bike", feature: 1 },
  { id: "02-home",              src: "02-home.html",             title: "Home",          state: "",                      feature: 1 },
  { id: "03-destination",       src: "03-destination.html",      title: "Destination",   state: "",                      feature: 1 },
  { id: "04-route",             src: "04-route.html",            title: "Route",         state: "Balanced",              feature: 2 },
  { id: "05-route-detail",      src: "05-route-detail.html",     title: "Route detail",  state: "Most fun",              feature: 3 },
  { id: "06-voice-live",        src: "06-voice.html",            title: "Companion",     state: "Conversation",          feature: 4 },
  { id: "06-voice-done",        src: "06-voice.html#done",       title: "Companion",     state: "Trip ready",            feature: 5 },
  { id: "07-trip",              src: "07-trip.html",             title: "Alpine Loop",   state: "3 days",                feature: 6 },
  { id: "07-trip-swap",         src: "07-trip.html#swap",        title: "Alpine Loop",   state: "Swap a segment",        feature: 6 },
  { id: "08-explore",           src: "08-explore.html",          title: "Explore",       state: "Segments",              feature: 7 },
  { id: "08-explore-heat",      src: "08-explore.html#heat",     title: "Explore",       state: "Heat map",              feature: 7 },
  { id: "09-segment",           src: "09-segment.html",          title: "Segment",       state: "Kesselberg by Marco_K", feature: 8 },
  { id: "10-ride-mode",         src: "10-ride-mode.html",        title: "Ride mode",     state: "Navigation",            feature: 9 },
  { id: "10-ride-mode-bike",    src: "10-ride-mode.html#bike",   title: "Bike display",  state: "10.25\" TFT",           feature: 9, tft: true },
  { id: "10-ride-mode-feedback", src: "10-ride-mode.html#feedback", title: "Ride mode",  state: "Feedback card",         feature: 10 },
  { id: "11-recap",             src: "11-recap.html",            title: "Ride complete", state: "",                      feature: 10 },
  { id: "12-profile",           src: "12-profile.html",          title: "Profile",       state: "",                      feature: 5 },
];

/* target : index dans RIDE_SEQUENCE de l'écran ouvert au clic. */
const RIDE_FEATURES = [
  { n: 1,  title: "Two ways to ride: Go somewhere or Plan a trip",                                   screens: "02, 03",          target: "02-home" },
  { n: 2,  title: "Fast ↔ Fun slider that reshapes your route live",                                 screens: "04",              target: "04-route" },
  { n: 3,  title: "Weather-aware routing with departure advice",                                     screens: "04, 05",          target: "05-route-detail" },
  { n: 4,  title: "Voice trip planner, a five-minute conversation",                                  screens: "06",              target: "06-voice-live" },
  { n: 5,  title: "A companion that learns your riding preferences",                                 screens: "06, 12",          target: "06-voice-done" },
  { n: 6,  title: "Multi-day trip generation with swappable segments",                               screens: "07, 07 · swap",   target: "07-trip" },
  { n: 7,  title: "Community segments rated by real riders",                                         screens: "08, 08 · heat",   target: "08-explore" },
  { n: 8,  title: "Follow a rider's segment instead of trusting an AI blindly",                      screens: "09",              target: "09-segment" },
  { n: 9,  title: "Ride mode and bike display, glove-friendly",                                      screens: "10, 10 · TFT",    target: "10-ride-mode" },
  { n: 10, title: "In-ride feedback and ride recap that make the whole community smarter",           screens: "10 · feedback, 11", target: "10-ride-mode-feedback" },
];
