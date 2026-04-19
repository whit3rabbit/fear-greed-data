#!/usr/bin/env python3
"""Convert a macromicro.me chart dump into the macromicro fear-greed CSV.

One-shot helper. Not part of CI because macromicro requires a logged-in
session - the raw JSON must be captured manually from the Network tab at
https://en.macromicro.me/charts/data/50108 and saved to json/macromicro.json.

The JSON shape is:
    { "data": { "c:50108": { "series": [ [[date, value], ...], ... ] } } }

series[0] is the Fear & Greed series; series[1] is a companion price series
(ignored). Values are strings like "35.6000"; we keep them as floats.

Usage:
    python scripts/convert_macromicro.py             # uses default paths
    python scripts/convert_macromicro.py path/to.json path/out.csv
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_IN = REPO_ROOT / "json" / "macromicro.json"
DEFAULT_OUT = REPO_ROOT / "datasets" / "macromicro_fear_greed_data.csv"


def convert(in_path: Path, out_path: Path) -> int:
    payload = json.loads(in_path.read_text())
    series = payload["data"]["c:50108"]["series"][0]
    rows = [(date, float(value)) for date, value in series]
    rows.sort(key=lambda r: r[0])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Date", "Fear Greed"])
        w.writerows(rows)

    print(f"Wrote {len(rows)} rows to {out_path.relative_to(REPO_ROOT)}")
    print(f"Range: {rows[0][0]} -> {rows[-1][0]}")
    return 0


def main(argv: list[str]) -> int:
    in_path = Path(argv[1]) if len(argv) > 1 else DEFAULT_IN
    out_path = Path(argv[2]) if len(argv) > 2 else DEFAULT_OUT
    return convert(in_path, out_path)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
