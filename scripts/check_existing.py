"""Check whether a candidate key or string already exists in the current
Hubble localization JSON (hubble_ko-KR / ja-JP / en-US).

The JSON is two-level: { key1: { key2: value, ... }, ... } (plus rare
top-level string entries). Use this BEFORE creating a new key so duplicates
are excluded and existing translations are reused.

String matching normalizes whitespace and a few punctuation marks (ported from
the project's intersect.py norm()) so that near-identical copy still matches.

Usage:
  # does a Korean string already exist anywhere?
  python3 check_existing.py --hubble-dir <dir> --kr "AI 옵티마이저" --kr "X축"

  # would this key collide?
  python3 check_existing.py --hubble-dir <dir> --key aiOptimizer.userInterestTitle
"""
import argparse
import json
import re
from pathlib import Path

LANGS = {"kr": "hubble_ko-KR.json", "jp": "hubble_ja-JP.json", "us": "hubble_en-US.json"}


def norm(s: str) -> str:
    # collapse whitespace, dots, and zero-width space (ported from intersect.py)
    return re.sub(r"[\s\.​]+", "", s or "").lower()


def load(hubble_dir: Path, fname: str) -> dict:
    p = hubble_dir / fname
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def flatten(d: dict) -> dict[str, str]:
    """{key1.key2: value} flat map (skips non-dict top-level entries)."""
    flat = {}
    for k1, v1 in d.items():
        if isinstance(v1, dict):
            for k2, v2 in v1.items():
                if isinstance(v2, str):
                    flat[f"{k1}.{k2}"] = v2
        elif isinstance(v1, str):
            flat[k1] = v1
    return flat


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--hubble-dir", required=True, help="dir with hubble_*.json")
    ap.add_argument("--kr", action="append", default=[], help="Korean string(s) to look up")
    ap.add_argument("--key", action="append", default=[], help="key1.key2 to check for collision")
    args = ap.parse_args()

    hubble_dir = Path(args.hubble_dir)
    flat = {lang: flatten(load(hubble_dir, f)) for lang, f in LANGS.items()}
    # reverse index of normalized KR value -> list of key paths
    kr_rev: dict[str, list[str]] = {}
    for path, val in flat["kr"].items():
        kr_rev.setdefault(norm(val), []).append(path)

    hit = False

    for s in args.kr:
        paths = kr_rev.get(norm(s), [])
        if paths:
            hit = True
            print(f"[DUP] KR {s!r} already exists at: {', '.join(paths)}")
            for p in paths:
                jp = flat["jp"].get(p, "—")
                us = flat["us"].get(p, "—")
                print(f"        reuse → JP: {jp!r}  US: {us!r}")
        else:
            print(f"[NEW] KR {s!r} not found — safe to create")

    for k in args.key:
        if k in flat["kr"] or k in flat["jp"] or k in flat["us"]:
            hit = True
            print(f"[DUP] key {k} already exists (KR: {flat['kr'].get(k, '—')!r})")
        else:
            print(f"[NEW] key {k} free")

    raise SystemExit(1 if hit else 0)


if __name__ == "__main__":
    main()
