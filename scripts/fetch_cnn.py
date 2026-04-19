#!/usr/bin/env python3
"""Fetch CNN Fear & Greed Index historical data.

Hits https://production.dataviz.cnn.io/index/fearandgreed/graphdata/<start-date>
and writes:
  - json/cnn_output.json       raw response (for audit)
  - datasets/cnn_fear_greed.csv  parsed rows: Date (ISO), Fear Greed, Rating

The endpoint returns the full history from <start-date> to today in one call,
so this script is idempotent - re-running it simply refreshes the tail.
"""
from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

# CNN considers its historical data accurate from 2021-02-01 onward.
START_DATE = "2021-02-01"
URL = f"https://production.dataviz.cnn.io/index/fearandgreed/graphdata/{START_DATE}"

# CNN returns 418/403 for the default python-requests UA.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.cnn.com",
    "Referer": "https://www.cnn.com/",
}

REPO_ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = REPO_ROOT / "json" / "cnn_output.json"
CSV_PATH = REPO_ROOT / "datasets" / "cnn_fear_greed.csv"


def fetch() -> dict:
    resp = requests.get(URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()


def parse(payload: dict) -> list[tuple[str, float, str]]:
    hist = payload.get("fear_and_greed_historical") or {}
    data = hist.get("data") or []
    if not data:
        raise RuntimeError("CNN response missing fear_and_greed_historical.data")

    rows: list[tuple[str, float, str]] = []
    for entry in data:
        ts_ms = entry["x"]
        score = float(entry["y"])
        rating = entry.get("rating", "")
        d = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).date()
        rows.append((d.isoformat(), score, rating))

    # Endpoint usually returns sorted data, but don't rely on it.
    rows.sort(key=lambda r: r[0])
    return rows


def write_outputs(payload: dict, rows: list[tuple[str, float, str]]) -> None:
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

    with JSON_PATH.open("w") as f:
        json.dump(payload, f, indent=2)

    with CSV_PATH.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Date", "Fear Greed", "Rating"])
        w.writerows(rows)


def main() -> int:
    payload = fetch()
    rows = parse(payload)
    write_outputs(payload, rows)
    print(f"Wrote {len(rows)} rows to {CSV_PATH.relative_to(REPO_ROOT)}")
    print(f"Range: {rows[0][0]} -> {rows[-1][0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
