"""Generate a review-only <feature>_keys.csv of NEW localization keys.

Mirrors the 34-column header of the project sheet (e.g. aiOptimizer_sheet.csv)
and places each new key/translation row at the fixed column indices used by the
ListeningMind Hubble localization sheet. Generalized from make_plan_keys.py and
make_axis_legend_keys.py.

Spec file (JSON): a list of rows, each an object with fields:
  loc2  (위치2, required)   key1 (required)   key2 (required)
  kr, jp, us (translations, required)
  memo  (메모, optional)    note (삭제무방 및 비고 / dedup reason, optional)
  key3  (optional)          loc1 (위치1 override, optional)

Usage:
  python3 make_keys.py --template aiOptimizer_sheet.csv \
      --spec feature_spec.json --out feature_keys.csv \
      --loc1 "AI 옵티마이저" --date 2026-06-25
"""
import argparse
import csv
import json
from pathlib import Path

# Fixed column indices in the 34-column Hubble localization sheet.
COL = {
    "loc1": 0,   # 위치1
    "loc2": 1,   # 위치2
    "date": 2,   # 작성일
    "worker": 3, # 작업자
    "memo": 4,   # 메모
    "note": 5,   # 삭제무방 및 비고 (dedup/exclusion reason)
    "key1": 6,   # key1
    "key2": 7,   # key2
    "key3": 8,   # key3
    "kr": 9,     # KR
    "jp": 10,    # JP
    "us": 11,    # US
}


def read_header(template: Path) -> list[str]:
    with template.open(encoding="utf-8") as f:
        return next(csv.reader(f))


def build_rows(spec: list[dict], header: list[str], loc1: str, date: str) -> list[list[str]]:
    ncol = len(header)
    rows = [header]
    for item in spec:
        r = [""] * ncol
        r[COL["loc1"]] = item.get("loc1", loc1)
        r[COL["loc2"]] = item.get("loc2", "")
        r[COL["date"]] = item.get("date", date)
        r[COL["memo"]] = item.get("memo", "")
        r[COL["note"]] = item.get("note", "")
        r[COL["key1"]] = item.get("key1", "")
        r[COL["key2"]] = item.get("key2", "")
        r[COL["key3"]] = item.get("key3", "")
        r[COL["kr"]] = item.get("kr", "")
        r[COL["jp"]] = item.get("jp", "")
        r[COL["us"]] = item.get("us", "")
        rows.append(r)
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--template", required=True, help="34-column header source CSV")
    ap.add_argument("--spec", required=True, help="JSON list of new key rows")
    ap.add_argument("--out", required=True, help="output CSV path")
    ap.add_argument("--loc1", default="AI 옵티마이저", help="default 위치1 value")
    ap.add_argument("--date", default="", help="default 작성일 (YYYY-MM-DD)")
    args = ap.parse_args()

    header = read_header(Path(args.template))
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    if not isinstance(spec, list):
        raise SystemExit("spec must be a JSON list of row objects")

    rows = build_rows(spec, header, args.loc1, args.date)
    with Path(args.out).open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)

    print(f"wrote {args.out}: NEW={len(spec)} rows, cols={len(header)}")


if __name__ == "__main__":
    main()
