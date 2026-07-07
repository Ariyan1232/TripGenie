"""
Destination voting.

Each traveler submits a list of destinations they're willing to go to.
This module finds the destinations everyone agreed on, scores each one
using the date search + solver, and returns a ranked comparison so the
group can make an informed decision together.

Only destinations that every traveler voted for are considered -- nobody
gets taken somewhere they didn't agree to.
"""

from .models import Traveler, DestinationResult
from .airports import AIRPORTS
from .date_search import search_dates


def agreed_destinations(travelers: list[Traveler]) -> list[str]:
    """
    Return the airport codes that every traveler voted for.
    Sorted by total vote count, most popular first.
    """
    if not travelers:
        return []

    agreed = set(travelers[0].destination_votes)
    for t in travelers[1:]:
        agreed &= set(t.destination_votes)

    vote_counts = {}
    for t in travelers:
        for dest in t.destination_votes:
            if dest in agreed:
                vote_counts[dest] = vote_counts.get(dest, 0) + 1

    return sorted(agreed, key=lambda d: -vote_counts[d])


def compare_destinations(travelers: list[Traveler]) -> list[DestinationResult]:
    """
    For each destination everyone agreed on, run the date search
    and return a DestinationResult with all three labeled options.

    Results are sorted by best synced arrival spread (tightest sync first).
    """
    destinations = agreed_destinations(travelers)
    if not destinations:
        return []

    results = []
    for dest_code in destinations:
        options = search_dates(travelers, destination=dest_code)
        if not options:
            continue

        vote_count = sum(
            1 for t in travelers if dest_code in t.destination_votes
        )
        city_name = AIRPORTS.get(dest_code, {}).get("city", dest_code)

        results.append(DestinationResult(
            destination=dest_code,
            city_name=city_name,
            vote_count=vote_count,
            options=options,
        ))

    results.sort(key=lambda r: r.best_synced.spread_hours)
    return results