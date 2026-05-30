"""Tests for scripts/build_combined.py.

Covers the three load-bearing functions:

- ``rating_for`` — band-cutoff boundaries (half-open: [25, 45) etc.)
- ``combine`` — CNN wins on duplicate dates, sort ascending, fill ratings
- ``sanity_check`` — refuses to write on shorter/duplicate/stale output
"""

from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import pytest
from build_combined import combine, rating_for, sanity_check


# rating_for boundaries — half-open per the existing code's comment


@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (0, "extreme fear"),
        (24.99, "extreme fear"),
        (25, "fear"),
        (44.99, "fear"),
        (45, "neutral"),
        (54.99, "neutral"),
        (55, "greed"),
        (74.99, "greed"),
        (75, "extreme greed"),
        (100, "extreme greed"),
    ],
)
def test_rating_for_band_boundaries(score: float, expected: str) -> None:
    assert rating_for(score) == expected


# combine — CNN must win on overlap; output sorted ascending


def test_combine_cnn_wins_on_duplicate_dates() -> None:
    archive = pd.DataFrame(
        {"Date": ["2020-12-31"], "Fear Greed": [50.0], "Rating": [""]}
    )
    cnn = pd.DataFrame(
        {"Date": ["2020-12-31"], "Fear Greed": [99.0], "Rating": ["extreme greed"]}
    )

    combined = combine(archive, cnn)

    assert len(combined) == 1
    assert combined["Fear Greed"].iloc[0] == 99.0
    assert combined["Rating"].iloc[0] == "extreme greed"


def test_combine_sorts_ascending_and_fills_blank_ratings() -> None:
    archive = pd.DataFrame(
        {
            "Date": ["2020-12-31", "2019-06-15"],
            "Fear Greed": [10.0, 60.0],
            "Rating": ["", ""],
        }
    )
    cnn = pd.DataFrame(
        {"Date": ["2021-02-01"], "Fear Greed": [50.5], "Rating": ["neutral"]}
    )

    combined = combine(archive, cnn)

    assert list(combined["Date"]) == ["2019-06-15", "2020-12-31", "2021-02-01"]
    # Archive blank ratings are filled from rating_for; CNN ratings preserved
    assert combined["Rating"].iloc[0] == "greed"  # rating_for(60.0)
    assert combined["Rating"].iloc[1] == "extreme fear"  # rating_for(10.0)
    assert combined["Rating"].iloc[2] == "neutral"  # CNN-supplied


# sanity_check — three failure modes + a passing case


def test_sanity_check_raises_when_shorter_than_archive() -> None:
    combined = pd.DataFrame(
        {"Date": [date.today().isoformat()], "Fear Greed": [50.0], "Rating": ["neutral"]}
    )
    with pytest.raises(RuntimeError, match="shorter than archive"):
        sanity_check(combined, archive_len=10)


def test_sanity_check_raises_on_duplicate_dates() -> None:
    today = date.today().isoformat()
    combined = pd.DataFrame(
        {
            "Date": [today, today],
            "Fear Greed": [50.0, 50.0],
            "Rating": ["neutral", "neutral"],
        }
    )
    with pytest.raises(RuntimeError, match="Duplicate"):
        sanity_check(combined, archive_len=1)


def test_sanity_check_raises_when_stale() -> None:
    stale = (date.today() - timedelta(days=10)).isoformat()
    combined = pd.DataFrame(
        {"Date": [stale], "Fear Greed": [50.0], "Rating": ["neutral"]}
    )
    with pytest.raises(RuntimeError, match="days old"):
        sanity_check(combined, archive_len=1)


def test_sanity_check_passes_within_limit() -> None:
    combined = pd.DataFrame(
        {"Date": [date.today().isoformat()], "Fear Greed": [50.0], "Rating": ["neutral"]}
    )
    # No raise = pass
    sanity_check(combined, archive_len=1)
