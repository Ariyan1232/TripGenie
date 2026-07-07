"""
Tests for solver.py.

Covers: correct number of results, correct labels, that Cheapest
truly has the lowest cost, that Best synced truly has the smallest
spread, and that the scores stored on each result match what you'd
compute directly from the flights.
"""

from datetime import date

from converge.mock_flights import search_flights
from converge.solver import arrival_spread_hours, find_options


def get_options():
    return [
        search_flights("JFK", "BKK", date(2026, 10, 1)),
        search_flights("LHR", "BKK", date(2026, 10, 1)),
        search_flights("NRT", "BKK", date(2026, 10, 1)),
    ]


def test_find_options_returns_three_results():
    results = find_options(get_options())
    assert len(results) == 3


def test_labels_are_correct():
    results = find_options(get_options())
    labels = [r.label for r in results]
    assert "Cheapest" in labels
    assert "Best synced" in labels
    assert "Most balanced" in labels


def test_cheapest_has_lowest_cost():
    results = find_options(get_options())
    cheapest = next(r for r in results if r.label == "Cheapest")
    for other in results:
        assert cheapest.total_cost <= other.total_cost


def test_best_synced_has_smallest_spread():
    results = find_options(get_options())
    synced = next(r for r in results if r.label == "Best synced")
    for other in results:
        assert synced.spread_hours <= other.spread_hours


def test_each_result_has_one_flight_per_traveler():
    options = get_options()
    results = find_options(options)
    for r in results:
        assert len(r.flights) == len(options)


def test_scores_match_actual_flights():
    """SolverResult.total_cost and .spread_hours must match what you'd
    compute yourself from the flights -- they're not allowed to be stale."""
    results = find_options(get_options())
    for r in results:
        assert abs(r.total_cost - sum(f.price_usd for f in r.flights)) < 0.01
        assert abs(r.spread_hours - arrival_spread_hours(r.flights)) < 0.01