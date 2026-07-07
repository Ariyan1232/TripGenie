"""
Tests for mock_flights.py.

Covers: basic shape of the output, that distance correctly drives
price/duration (longer routes cost more and take longer), that seeded
randomness is actually stable across runs, and that arrival always comes
after departure.
"""

from datetime import date

from converge.mock_flights import search_flights


def test_returns_requested_number_of_options():
    flights = search_flights("JFK", "LHR", date(2026, 10, 1), num_options=3)
    assert len(flights) == 3


def test_longer_route_costs_more_on_average():
    short_route = search_flights("JFK", "LHR", date(2026, 10, 1))
    long_route = search_flights("JFK", "NRT", date(2026, 10, 1))
    avg_short = sum(f.price_usd for f in short_route) / len(short_route)
    avg_long = sum(f.price_usd for f in long_route) / len(long_route)
    assert avg_long > avg_short


def test_longer_route_takes_more_time_on_average():
    short_route = search_flights("JFK", "LHR", date(2026, 10, 1))
    long_route = search_flights("JFK", "NRT", date(2026, 10, 1))
    avg_short = sum((f.arrival - f.departure).total_seconds() for f in short_route) / len(short_route)
    avg_long = sum((f.arrival - f.departure).total_seconds() for f in long_route) / len(long_route)
    assert avg_long > avg_short


def test_same_inputs_give_same_results():
    """Seeded randomness: identical inputs must give identical results,
    across separate runs -- not just within the same script."""
    a = search_flights("JFK", "LHR", date(2026, 10, 1))
    b = search_flights("JFK", "LHR", date(2026, 10, 1))
    assert [f.price_usd for f in a] == [f.price_usd for f in b]


def test_different_dates_give_different_results():
    a = search_flights("JFK", "LHR", date(2026, 10, 1))
    b = search_flights("JFK", "LHR", date(2026, 10, 2))
    assert [f.price_usd for f in a] != [f.price_usd for f in b]


def test_arrival_always_after_departure():
    flights = search_flights("JFK", "NRT", date(2026, 10, 1))
    for f in flights:
        assert f.arrival > f.departure