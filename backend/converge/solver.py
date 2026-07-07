"""
The solver.

Given flight options per traveler and a shared destination, find the
combination (one flight per traveler) that best serves the group across
three different definitions of "best":

  Cheapest      -- minimize total group cost
  Best synced   -- minimize arrival spread (how far apart everyone lands)
  Most balanced -- best tradeoff between cost and sync

Returns all three as labeled SolverResult objects so the group can
compare and choose, rather than the app picking one answer for them.
"""

from itertools import product

from .models import Flight, SolverResult


def arrival_spread_hours(flights: list[Flight]) -> float:
    """
    How spread out are the arrivals in this group?

    Returns the gap in hours between the earliest and latest arrival.
    Zero means everyone lands at the same moment.
    """
    arrivals = [f.arrival for f in flights]
    earliest = min(arrivals)
    latest = max(arrivals)
    return (latest - earliest).total_seconds() / 3600


def find_options(
    options_per_traveler: list[list[Flight]],
) -> list[SolverResult]:
    """
    Given flight options per traveler, return three labeled combinations:
    Cheapest, Best synced, and Most balanced.

    options_per_traveler[0] = first traveler's flight options
    options_per_traveler[1] = second traveler's flight options
    ... and so on.
    """
    all_combos = [list(combo) for combo in product(*options_per_traveler)]

    if not all_combos:
        return []

    scored = [
        {
            "flights": combo,
            "spread": arrival_spread_hours(combo),
            "cost": sum(f.price_usd for f in combo),
        }
        for combo in all_combos
    ]

    # --- Cheapest ---
    cheapest = min(scored, key=lambda s: s["cost"])

    # --- Best synced ---
    synced = min(scored, key=lambda s: s["spread"])

    # --- Most balanced ---
    # Normalize both dimensions to 0-1 so neither cost nor sync
    # dominates the balance score. 0 = best seen, 1 = worst seen.
    min_spread = min(s["spread"] for s in scored)
    max_spread = max(s["spread"] for s in scored)
    min_cost   = min(s["cost"]   for s in scored)
    max_cost   = max(s["cost"]   for s in scored)

    spread_range = max_spread - min_spread or 1
    cost_range   = max_cost   - min_cost   or 1

    def balance_score(s):
        norm_spread = (s["spread"] - min_spread) / spread_range
        norm_cost   = (s["cost"]   - min_cost)   / cost_range
        return norm_spread + norm_cost

    balanced = min(scored, key=balance_score)

    return [
        SolverResult(
            label="Cheapest",
            flights=cheapest["flights"],
            spread_hours=cheapest["spread"],
            total_cost=cheapest["cost"],
        ),
        SolverResult(
            label="Best synced",
            flights=synced["flights"],
            spread_hours=synced["spread"],
            total_cost=synced["cost"],
        ),
        SolverResult(
            label="Most balanced",
            flights=balanced["flights"],
            spread_hours=balanced["spread"],
            total_cost=balanced["cost"],
        ),
    ]