"""
Tests for voting.py.

Covers: unanimous-only filtering, empty cases, sort order,
city name population, and that each result carries all three
solver options.
"""

from datetime import date

from converge.models import Traveler
from converge.voting import agreed_destinations, compare_destinations


def make_traveler(id_, origin, votes,
                  earliest=date(2026, 10, 1),
                  latest=date(2026, 10, 20)):
    return Traveler(
        id=id_, name=id_.title(), origin_airport=origin,
        earliest_departure=earliest, latest_return=latest,
        destination_votes=votes,
    )


def test_agreed_destinations_unanimous_only():
    travelers = [
        make_traveler("a", "JFK", ["NRT", "BKK", "SIN"]),
        make_traveler("b", "LHR", ["NRT", "BKK", "DXB"]),
        make_traveler("c", "NRT", ["BKK", "SIN", "NRT"]),
    ]
    agreed = agreed_destinations(travelers)
    assert set(agreed) == {"NRT", "BKK"}
    assert "SIN" not in agreed
    assert "DXB" not in agreed


def test_agreed_destinations_empty_when_no_overlap():
    travelers = [
        make_traveler("a", "JFK", ["NRT"]),
        make_traveler("b", "LHR", ["BKK"]),
    ]
    assert agreed_destinations(travelers) == []


def test_agreed_destinations_single_traveler():
    travelers = [make_traveler("a", "JFK", ["NRT", "BKK"])]
    agreed = agreed_destinations(travelers)
    assert set(agreed) == {"NRT", "BKK"}


def test_compare_destinations_only_returns_agreed():
    travelers = [
        make_traveler("a", "JFK", ["NRT", "BKK", "SIN"]),
        make_traveler("b", "LHR", ["NRT", "BKK"]),
    ]
    results = compare_destinations(travelers)
    codes = {r.destination for r in results}
    assert "NRT" in codes
    assert "BKK" in codes
    assert "SIN" not in codes


def test_compare_destinations_sorted_by_sync():
    travelers = [
        make_traveler("a", "JFK", ["NRT", "BKK"]),
        make_traveler("b", "LHR", ["NRT", "BKK"]),
    ]
    results = compare_destinations(travelers)
    spreads = [r.best_synced.spread_hours for r in results]
    assert spreads == sorted(spreads)


def test_each_result_has_three_options():
    travelers = [
        make_traveler("a", "JFK", ["BKK"]),
        make_traveler("b", "LHR", ["BKK"]),
    ]
    results = compare_destinations(travelers)
    assert len(results) == 1
    assert len(results[0].options) == 3


def test_city_name_populated():
    travelers = [
        make_traveler("a", "JFK", ["NRT"]),
        make_traveler("b", "LHR", ["NRT"]),
    ]
    results = compare_destinations(travelers)
    assert results[0].city_name == "Tokyo"


def test_no_votes_returns_empty():
    travelers = [
        make_traveler("a", "JFK", []),
        make_traveler("b", "LHR", []),
    ]
    assert compare_destinations(travelers) == []