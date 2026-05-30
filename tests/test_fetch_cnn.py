"""Tests for scripts/fetch_cnn.py.

Covers ``parse`` only — the side-effecting ``fetch`` and ``write_outputs``
are exercised by the workflow integration; unit-testing them adds little
beyond what's already proved by ``write_outputs``'s use of stdlib ``csv``
and ``json`` writers.

Synthetic CNN payloads use a few real-world UTC millisecond timestamps
so the date conversion is exercised end-to-end without needing to mock
``datetime``.
"""

from __future__ import annotations

import pytest
from fetch_cnn import parse


def test_parse_happy_path_two_rows() -> None:
    payload = {
        "fear_and_greed_historical": {
            "data": [
                {"x": 1612137600000, "y": 33.5, "rating": "fear"},  # 2021-02-01
                {"x": 1612224000000, "y": 50.0, "rating": "neutral"},  # 2021-02-02
            ]
        }
    }

    rows = parse(payload)

    assert rows == [
        ("2021-02-01", 33.5, "fear"),
        ("2021-02-02", 50.0, "neutral"),
    ]


def test_parse_sorts_unsorted_input_ascending() -> None:
    payload = {
        "fear_and_greed_historical": {
            "data": [
                {"x": 1612224000000, "y": 50.0, "rating": "neutral"},  # 2021-02-02
                {"x": 1612137600000, "y": 33.5, "rating": "fear"},  # 2021-02-01
            ]
        }
    }

    rows = parse(payload)

    assert [r[0] for r in rows] == ["2021-02-01", "2021-02-02"]


def test_parse_missing_historical_block_raises() -> None:
    with pytest.raises(RuntimeError, match="missing"):
        parse({})


def test_parse_empty_data_array_raises() -> None:
    with pytest.raises(RuntimeError, match="missing"):
        parse({"fear_and_greed_historical": {"data": []}})


def test_parse_defaults_missing_rating_to_empty_string() -> None:
    payload = {
        "fear_and_greed_historical": {
            "data": [{"x": 1612137600000, "y": 33.5}],
        }
    }

    rows = parse(payload)

    assert rows == [("2021-02-01", 33.5, "")]
