/* RIDE by BMW Motorrad — les 10 features de la démo et la séquence des écrans (SCREENS.md §10 features).
   Source unique pour index.html (galerie) et scripts/export_pdf.py (PDF). Aucune dépendance. */

/* Chaque entrée : id (nom de PNG dans out/), src (ce que la galerie charge : l'animation quand elle existe),
   title, state (lisible), feature (numéro), tft (artboard 1920×720 dans le cadre tableau de bord). */
/* Sélection de consultation (Tim, 13 sept. 2026) : 9 maquettes. Les autres écrans restent dans screens/ et se
   capturent toujours avec shot.py, mais ne sont ni dans la galerie ni dans le PDF. */
const RIDE_SEQUENCE = [
  { id: "03-destination",       src: "03-destination.html",      title: "Destination",   state: "",                      feature: 1 },
  { id: "04-route",             src: "04-route.html",            title: "Route",         state: "Balanced",              feature: 2 },
  { id: "06-voice-live",        src: "06-voice.html",            title: "Companion",     state: "Conversation",          feature: 4 },
  { id: "06-voice-done",        src: "06-voice.html#done",       title: "Companion",     state: "Trip ready",            feature: 5 },
  { id: "07-trip-swap",         src: "07-trip.html#swap",        title: "Alpine Loop",   state: "Swap a segment",        feature: 6 },
  { id: "08-explore",           src: "08-explore.html",          title: "Explore",       state: "Segments",              feature: 7 },
  { id: "09-segment",           src: "09-segment.html",          title: "Segment",       state: "Kesselberg by Marco_K", feature: 8 },
  { id: "11-recap",             src: "11-recap.html",            title: "Ride complete", state: "",                      feature: 10 },
  { id: "12-profile",           src: "12-profile.html",          title: "Profile",       state: "",                      feature: 5 },
];

/* Écrans du TFT moto (On the bike) : artboards 1920×720, montrés seuls (.dash), 2 emplacements dans le PDF */
const RIDE_TFT = [
  { id: "tft-01-briefing",   src: "tft-01-briefing.html",   title: "Before you ride", state: "Bike on, synced with the app",  feature: 3,  tft: true },
  { id: "tft-02-navigation", src: "tft-02-navigation.html", title: "Navigation",      state: "Next turn, segments ahead",     feature: 9,  tft: true },
  { id: "tft-03-segment",    src: "tft-03-segment.html",    title: "Segment mode",    state: "Inside the Kesselberg",         feature: 8,  tft: true },
  { id: "tft-04-alert",      src: "tft-04-alert.html",      title: "Companion",       state: "Rain ahead, one decision",      feature: 3,  tft: true },
  { id: "tft-05-recap",      src: "tft-05-recap.html",      title: "Ride complete",   state: "Rate, then sent to the phone",  feature: 10, tft: true },
];
RIDE_SEQUENCE.push(...RIDE_TFT);

/* Écrans hors sélection, gardés pour référence (shot.py les capture toujours) */
const RIDE_EXTRA = ["01-splash#connected", "02-home", "05-route-detail", "07-trip", "08-explore#heat",
                    "10-ride-mode", "10-ride-mode#bike", "10-ride-mode#feedback"];

/* target : index dans RIDE_SEQUENCE de l'écran ouvert au clic. */
const RIDE_FEATURES = [
  { n: 1,  title: "Two ways to ride: Go somewhere or Plan a trip",                                   screens: "03",              target: "03-destination" },
  { n: 2,  title: "Fast ↔ Fun slider that reshapes your route live",                                 screens: "04",              target: "04-route" },
  { n: 3,  title: "Weather-aware routing with departure advice",                                     screens: "04",              target: "04-route" },
  { n: 4,  title: "Voice trip planner, a five-minute conversation",                                  screens: "06",              target: "06-voice-live" },
  { n: 5,  title: "A companion that learns your riding preferences",                                 screens: "06, 12",          target: "06-voice-done" },
  { n: 6,  title: "Multi-day trip generation with swappable segments",                               screens: "07 · swap",       target: "07-trip-swap" },
  { n: 7,  title: "Community segments rated by real riders",                                         screens: "08",              target: "08-explore" },
  { n: 8,  title: "Follow a rider's segment instead of trusting an AI blindly",                      screens: "09",              target: "09-segment" },
  { n: 9,  title: "Ride mode and bike display, glove-friendly",                                      screens: "11",              target: "11-recap" },
  { n: 10, title: "In-ride feedback and ride recap that make the whole community smarter",           screens: "11",              target: "11-recap" },
];
