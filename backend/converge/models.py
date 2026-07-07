"""
Step 1: the smallest possible model.

A Traveler is just: who they are, where they're flying from, and roughly
when they're free to travel. A Flight is one bookable leg, with real
timezone-aware departure/arrival times. Everything else (budget, layover
tolerance, destination votes) gets added later, once we have a reason to
need it.

Airport reference data (timezones, etc.) lives in airports.py, not here --
this file is just data shapes.
"""

from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Traveler:
    id: str
    name: str
    origin_airport: str  # IATA code, e.g. "JFK"
    earliest_departure: date
    latest_return: date


@dataclass
class Flight:
    origin: str        # IATA code
    destination: str   # IATA code
    departure: datetime  # timezone-aware, in the ORIGIN's local time
    arrival: datetime    # timezone-aware, in the DESTINATION's local time
    price_usd: float


@dataclass
class SolverResult:
    label: str           # "Cheapest", "Best synced", "Most balanced"
    flights: list[Flight]  # one Flight per traveler
    spread_hours: float  # arrival spread across the group
    total_cost: float    # sum of all flight prices