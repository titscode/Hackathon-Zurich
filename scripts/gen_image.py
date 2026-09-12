#!/usr/bin/env python3
"""Genere une image via l'API DeepInfra (compatible OpenAI) et l'ecrit sur disque.

    python scripts/gen_image.py "un bol de granola, vue du dessus" assets/granola.png
    python scripts/gen_image.py "texture papier" assets/bg.png --size 768x768 --seed 42

Cle API: variable d'environnement DEEPINFRA_API_KEY uniquement (jamais dans le repo).
"""
import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ENDPOINT = "https://api.deepinfra.com/v1/openai/images/generations"
DEFAULT_MODEL = "black-forest-labs/FLUX-1-schnell"  # le moins cher (~0.0005 $/image)


def post(url: str, payload: dict, token: str) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:800]
        sys.exit(f"erreur DeepInfra HTTP {e.code}: {body}")
    except urllib.error.URLError as e:
        sys.exit(f"erreur reseau: {e.reason}")


def image_bytes(item: dict) -> bytes:
    """La reponse expose soit b64_json, soit une url (selon le modele)."""
    if item.get("b64_json"):
        return base64.b64decode(item["b64_json"])
    url = item.get("url")
    if not url:
        sys.exit(f"reponse inattendue, ni b64_json ni url: {list(item)}")
    if url.startswith("data:"):
        return base64.b64decode(url.split(",", 1)[1])
    with urllib.request.urlopen(url, timeout=180) as resp:
        return resp.read()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("output", help="chemin du PNG, ex. assets/hero.png")
    ap.add_argument("--size", default="1024x1024", help="LARGEURxHAUTEUR")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--seed", type=int, help="pour un resultat reproductible")
    ap.add_argument("--steps", type=int, help="nombre d'etapes d'inference")
    args = ap.parse_args()

    token = os.environ.get("DEEPINFRA_API_KEY")
    if not token:
        sys.exit(
            "erreur: DEEPINFRA_API_KEY n'est pas definie.\n"
            '  Windows : setx DEEPINFRA_API_KEY "sk-..." puis rouvrir le terminal\n'
            '  bash    : export DEEPINFRA_API_KEY="sk-..."'
        )

    if "x" not in args.size:
        sys.exit("erreur: --size attend le format LARGEURxHAUTEUR, ex. 1024x1024")

    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "size": args.size,
        "n": 1,
    }
    if args.seed is not None:
        payload["seed"] = args.seed
    if args.steps is not None:
        payload["num_inference_steps"] = args.steps

    data = post(ENDPOINT, payload, token)
    items = data.get("data") or []
    if not items:
        sys.exit(f"reponse vide: {json.dumps(data)[:500]}")

    dst = Path(args.output)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(image_bytes(items[0]))
    print(f"{dst} ({dst.stat().st_size // 1024} Ko)")


if __name__ == "__main__":
    main()
