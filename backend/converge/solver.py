"""
Step 4: the solver.

Given N travelers, a shared destination, a shared date, and a few flight
options per traveler, find the combination of one flight per traveler that
minimizes the arrival spread -- the gap between the earliest and latest
landing in the group.

This is the core of what makes Converge different from just booking
flights independently: it optimizes for the group, not for each person
individually.
"""

from .models import Flight


def arrival_spread_hours(flights: list[Flight]) -> float:
    """
    How spread out are the arrivals in this group?

    Returns the gap in hours between the earliest and latest arrival.
    Zero means everyone lands at the same moment. Works correctly across
    timezones for the same reason arrival_gap_hours does -- Flight.arrival
    is timezone-aware, so comparing arrivals across different origin
    timezones gives the true elapsed gap.
    """
    arrivals = [f.arrival for f in flights]
    earliest = min(arrivals)
    latest = max(arrivals)
    return (latest - earliest).total_seconds() / 3600


def best_synced_combination(
    options_per_traveler: list[list[Flight]],
) -> list[Flight]:
    """
    Given a list of flight options per traveler, return the combination
    (one flight per traveler) that produces the smallest arrival spread.

    options_per_traveler[0] = Alice's flight options
    options_per_traveler[1] = Ben's flight options
    ... and so on.

    Returns one flight per traveler -- the best combination found.
    """
    from itertools import product

    best_combo = None
    best_spread = float("inf")

    for combo in product(*options_per_traveler):
        spread = arrival_spread_hours(list(combo))
        if spread < best_spread:
            best_spread = spread
            best_combo = list(combo)

    return best_combo