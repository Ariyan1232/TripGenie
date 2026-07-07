"""
Arrival sync checking.

Given two flights arriving at the same destination, how far apart do
they land? This is the core question the whole product is built around
-- "did everyone land around the same time?" -- expressed in its
simplest possible form: just two people, one number.

We'll generalize to N people and multiple destinations later. Starting
with two makes the logic easy to verify and test before adding complexity.
"""

from .models import Flight


def arrival_gap_hours(flight_a: Flight, flight_b: Flight) -> float:
    """
    How many hours apart do two flights arrive?

    Works correctly across timezones because Flight.arrival is a
    timezone-aware datetime -- subtracting two aware datetimes always
    gives the true elapsed time between them, regardless of what local
    time zones they're expressed in.
    """
    gap = flight_a.arrival - flight_b.arrival
    return abs(gap.total_seconds()) / 3600