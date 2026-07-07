"""
Date search.

Searches across every date in the group's availability overlap,
runs the solver for each date, and returns the single best result
per label (Cheapest, Best synced, Most balanced) across all dates.

This is what turns "find a good flight combination" into "find a
good flight combination AND a good date to travel" -- the two
decisions are solved together rather than separately.
"""

from datetime import date, timedelta

from .models import Traveler, SolverResult
from .mock_flights import search_flights
from .solver import find_options


def overlapping_dates(travelers: list[Traveler]) -> list[date]:
    """
    Find all dates where every traveler is available.
    Returns an empty list if no overlap exists.
    """
    earliest = max(t.earliest_departure for t in travelers)
    latest   = min(t.latest_return      for t in travelers)

    if earliest > latest:
        return []

    days = (latest - earliest).days + 1
    return [earliest + timedelta(days=i) for i in range(days)]


def search_dates(
    travelers: list[Traveler],
    destination: str,
) -> list[SolverResult]:
    """
    Search across the group's overlapping date window and return
    the best result per label found across all dates.

    Returns up to three SolverResults: Cheapest, Best synced,
    Most balanced -- each being the best version of that label
    found across every date searched.
    """
    dates = overlapping_dates(travelers)
    if not dates:
        return []

    best: dict[str, SolverResult] = {}

    for on_date in dates:
        options_per_traveler = [
            search_flights(t.origin_airport, destination, on_date)
            for t in travelers
        ]
        results = find_options(options_per_traveler)

        for result in results:
            label = result.label
            if label not in best:
                best[label] = result
                continue

            if label == "Cheapest" and result.total_cost < best[label].total_cost:
                best[label] = result
            elif label == "Best synced" and result.spread_hours < best[label].spread_hours:
                best[label] = result
            elif label == "Most balanced":
                curr = best[label]
                if (result.spread_hours + result.total_cost / 1000) < \
                   (curr.spread_hours   + curr.total_cost   / 1000):
                    best[label] = result

    return list(best.values())