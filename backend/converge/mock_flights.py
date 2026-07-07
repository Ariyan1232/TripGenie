"""
Mock flight search.

Generates a small list of Flight options for a given route and date,
standing in for a real flights API (Amadeus, Duffel, Skyscanner, etc.)
later. Price and duration are driven by distance_km(), so a long route
always costs more and takes longer than a short one -- the randomness
here only adds realistic noise on top of that, it never overrides it.

Uses seeded randomness: the same (origin, destination, date) always
produces the same results, across separate runs. This makes debugging
much easier -- if something looks wrong, you can reproduce it exactly
instead of chasing a one-off random fluke.
"""

import hashlib
import random
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from .airports import AIRPORTS
from .distance import distance_km
from .models import Flight


def _seed_for(origin: str, destination: str, on_date: date) -> int:
    """
    Turn a route + date into a stable integer seed.

    Important: Python's built-in hash() on strings is randomized every time
    you start a new Python process (a security feature, unrelated to our
    needs here) -- so it gives consistent results WITHIN one run, but
    different results EVERY time you restart Python. That defeats the
    point of seeding. hashlib.sha256 doesn't have this problem: same input
    string always produces the same hash, on every run, forever.
    """
    key = f"{origin}-{destination}-{on_date.isoformat()}"
    digest = hashlib.sha256(key.encode()).hexdigest()
    return int(digest, 16) % (2**32)


def search_flights(
    origin: str,
    destination: str,
    on_date: date,
    num_options: int = 3,
) -> list[Flight]:
    """Return a few mock Flight options for this route and date."""
    rng = random.Random(_seed_for(origin, destination, on_date))

    dist = distance_km(origin, destination)

    # Rough, made-up-but-plausible baseline: a little over $0.08/km, plus a
    # flat fee. A real flights API replaces this whole calculation later --
    # the only thing that matters here is that longer routes reliably cost
    # more and take longer than shorter ones.
    base_price = 60 + dist * 0.085
    base_duration_hours = dist / 800  # rough average cruise speed, in km/h

    origin_tz = ZoneInfo(AIRPORTS[origin]["timezone"])
    dest_tz = ZoneInfo(AIRPORTS[destination]["timezone"])

    flights = []
    for _ in range(num_options):
        # Small random variation around the baseline -- enough that options
        # differ from each other, not enough that a short route could
        # randomly come out pricier than a much longer one.
        price = round(base_price * rng.uniform(0.85, 1.25), 2)
        duration_hours = round(base_duration_hours * rng.uniform(0.95, 1.3), 2)

        # Pick a plausible departure hour, anchored in the origin's local time.
        departure_hour = rng.randint(6, 21)
        departure = datetime(
            on_date.year, on_date.month, on_date.day, departure_hour, 0,
            tzinfo=origin_tz,
        )

        # Compute arrival correctly: convert departure to an absolute instant
        # (UTC), add the flight duration, THEN convert into the
        # destination's local time. This is the same approach we proved
        # works back when we built Flight by hand.
        arrival_utc = departure.astimezone(ZoneInfo("UTC")) + timedelta(hours=duration_hours)
        arrival = arrival_utc.astimezone(dest_tz)

        flights.append(
            Flight(
                origin=origin,
                destination=destination,
                departure=departure,
                arrival=arrival,
                price_usd=price,
            )
        )

    return flights