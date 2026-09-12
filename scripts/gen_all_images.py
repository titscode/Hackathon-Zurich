#!/usr/bin/env python3
"""Genere en une passe toutes les images de RIDE (SCREENS.md, ordre de construction etape 2).

    python scripts/gen_all_images.py          # ne regenere pas ce qui existe
    python scripts/gen_all_images.py --force  # tout regenerer
"""
import subprocess, sys, pathlib
from concurrent.futures import ThreadPoolExecutor

ROOT = pathlib.Path(__file__).resolve().parent.parent
GEN = ROOT / "scripts" / "gen_image.py"

# DESIGN.md §5 : prefixe impose a toutes les photos.
BASE = ("photorealistic editorial photograph, muted cinematic color grading, "
        "soft directional light, no text, no logos, no people unless specified, ")

CARD = "1200x800"     # 3:2, cards
TALL = "768x1344"     # 9:16, plein ecran
AVA  = "512x512"      # avatars

JOBS = [
    # --- 10 routes / cols en 3:2 (les 8 segments communautaires + 2 dream rides)
    ("routes/kesselberg.png", CARD,
     "tight hairpin mountain road climbing above Kochelsee lake in the Bavarian Alps, "
     "wet dark asphalt, guardrail, steep forested slopes, low morning mist over the lake"),
    ("routes/sudelfeld.png", CARD,
     "sweeping alpine pass road with long curves through open mountain meadows, "
     "Bavarian Alps, overcast diffuse light, distant limestone peaks"),
    ("routes/tatzelwurm.png", CARD,
     "narrow forest pass road with tight switchbacks through dense dark conifers, "
     "Bavarian Alps, damp asphalt, shafts of light between trees"),
    ("routes/alpenstrasse.png", CARD,
     "lakeside road curving along the shore of an alpine lake between Tegernsee and Schliersee, "
     "calm dark water, wooded hills, soft overcast light"),
    ("routes/achenpass.png", CARD,
     "wide mountain pass road descending toward a turquoise alpine reservoir, "
     "Bavarian Austrian border, rocky slopes, moody grey sky"),
    ("routes/rossfeld.png", CARD,
     "high alpine panoramic ridge road above the clouds, Rossfeld Panoramastrasse, "
     "bare rock and grass, dramatic layered mountain silhouettes at dusk"),
    ("routes/oberjoch.png", CARD,
     "series of stacked hairpin bends on a forested alpine hillside seen from above, "
     "Allgau Alps, autumn colours, cool overcast light"),
    ("routes/kochelsee.png", CARD,
     "flat lakeside road running along the reedy shore of Kochelsee, Bavaria, "
     "still water reflecting mountains, early morning haze"),
    ("routes/stelvio.png", CARD,
     "iconic mountain pass with dozens of stacked hairpin switchbacks on a bare rocky slope, "
     "Stelvio pass north face, patches of snow, cold high altitude light"),
    ("routes/grimsel.png", CARD,
     "granite alpine pass road between dark rock walls and a deep blue reservoir, "
     "Grimsel pass Switzerland, stark bare stone, cold flat light"),
    # --- 2 photos complementaires en 3:2 (ecrans 02 et 08)
    ("routes/bavarian-morning.png", CARD,
     "empty rural two lane country road curving through Bavarian farmland at sunrise, "
     "rows of poplars, low golden mist over fields, distant Alps on the horizon"),
    ("routes/susten.png", CARD,
     "high alpine pass road winding across a barren rocky plateau under a vast sky, "
     "Susten pass Switzerland, glacier visible in the distance, cold clear light"),
    # --- 2 photos 9:16
    ("routes/kesselberg-tall.png", TALL,
     "vertical view up a steep hairpin mountain road cut into a forested slope above an alpine lake, "
     "Kesselberg Bavaria, wet dark asphalt, guardrail, mist in the trees"),
    ("routes/alpine-pass-tall.png", TALL,
     "vertical view of a winding alpine pass road climbing toward a high rocky col, "
     "layered mountain ridges, cold blue hour light, empty road"),
    # --- 8 avatars
    ("avatars/marco-k.png", AVA,
     "head and shoulders portrait of a man in his late thirties, short dark hair, "
     "short beard, slight smile, plain dark grey studio background, soft key light"),
    ("avatars/alpine-anna.png", AVA,
     "head and shoulders portrait of a woman in her early thirties, blonde hair tied back, "
     "slight smile, plain dark grey studio background, soft key light"),
    ("avatars/flo-r18.png", AVA,
     "head and shoulders portrait of a man in his twenties, curly brown hair, clean shaven, "
     "slight smile, plain dark grey studio background, soft key light"),
    ("avatars/lisa-gs.png", AVA,
     "head and shoulders portrait of a woman in her forties, short dark bob haircut, "
     "slight smile, plain dark grey studio background, soft key light"),
    ("avatars/jonas-b.png", AVA,
     "head and shoulders portrait of a man in his fifties, grey hair, glasses, "
     "slight smile, plain dark grey studio background, soft key light"),
    ("avatars/max-rt.png", AVA,
     "head and shoulders portrait of a man in his thirties, shaved head, stubble, "
     "neutral expression, plain dark grey studio background, soft key light"),
    ("avatars/stefan-w.png", AVA,
     "head and shoulders portrait of a man in his late twenties, dark hair, light beard, "
     "slight smile, plain dark grey studio background, soft key light"),
    ("avatars/tim.png", AVA,
     "head and shoulders portrait of a man in his early thirties, short brown hair, "
     "light stubble, calm confident expression, plain dark grey studio background, soft key light"),
]

force = "--force" in sys.argv


def run(job):
    rel, size, prompt = job
    dst = ROOT / "assets" / rel
    if dst.exists() and not force:
        return f"skip  {rel}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        [sys.executable, str(GEN), BASE + prompt, str(dst), "--size", size, "--seed", "11"],
        capture_output=True, text=True)
    if r.returncode != 0:
        return f"FAIL  {rel}: {(r.stderr or r.stdout).strip()[:160]}"
    return f"ok    {rel}  ({dst.stat().st_size // 1024} Ko)"


with ThreadPoolExecutor(max_workers=6) as pool:
    for line in pool.map(run, JOBS):
        print(line, flush=True)
