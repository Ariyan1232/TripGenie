"""
Tests for date_search.py.

Covers: overlap calculation, empty overlap, that results are returned
for each label, and that the Cheapest/Best synced invariants hold
across the full date window searched.
"""

from datetime import date

from converge.models import Traveler
from converge.date_search import overlapping_dates, search_dates


def make_traveler(id_, origin, earliest, latest):
    return Traveler(id=id_, name=id_.title(), origin_airport=origin,
                    earliest_departure=earliest, latest_return=latest)


def test_overlap_is_intersection_of_all_windows():
    travelers = [
        make_traveler("a", "JFK", date(2026, 10, 1), date(2026, 10, 20)),
        make_traveler("b", "LHR", date(2026, 10, 5), date(2026, 10, 25)),
        make_traveler("c", "NRT", date(2026, 10, 3), date(2026, 10, 18)),
    ]
    overlap = overlapping_dates(travelers)
    assert overlap[0]  == date(2026, 10, 5)
    assert overlap[-1] == date(2026, 10, 18)
    assert len(overlap) == 14


def test_no_overlap_returns_empty():
    travelers = [
        make_traveler("a", "JFK", date(2026, 10, 1),  date(2026, 10, 10)),
        make_traveler("b", "LHR", date(2026, 10, 15), date(2026, 10, 25)),
    ]
    assert overlapping_dates(travelers) == []


def test_search_dates_returns_three_results():
    travelers = [
        make_traveler("a", "JFK", date(2026, 10, 1), date(2026, 10, 20)),
        make_traveler("b", "LHR", date(2026, 10, 1), date(2026, 10, 20)),
    ]
    results = search_dates(travelers, destination="BKK")
    assert len(results) == 3


def test_search_dates_empty_when_no_overlap():
    travelers = [
        make_traveler("a", "JFK", date(2026, 10, 1),  date(2026, 10, 5)),
        make_traveler("b", "LHR", date(2026, 10, 15), date(2026, 10, 20)),
    ]
    results = search_dates(travelers, destination="BKK")
    assert results == []


def test_cheapest_result_is_cheapest_across_all_dates():
    travelers = [
        make_traveler("a", "JFK", date(2026, 10, 1), date(2026, 10, 20)),
        make_traveler("b", "LHR", date(2026, 10, 1), date(2026, 10, 20)),
    ]
    results = search_dates(travelers, destination="BKK")
    cheapest = next(r for r in results if r.label == "Cheapest")
    for other in results:
        assert cheapest.total_cost <= other.total_cost


def test_best_synced_has_tightest_spread_across_all_dates():
    travelers = [
        make_traveler("a", "JFK", date(2026, 10, 1), date(2026, 10, 20)),
        make_traveler("b", "LHR", date(2026, 10, 1), date(2026, 10, 20)),
    ]
    results = search_dates(travelers, destination="BKK")
    synced = next(r for r in results if r.label == "Best synced")
    for other in results:
        assert synced.spread_hours <= other.spread_hours