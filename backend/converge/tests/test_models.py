"""
Tests for models.py.

Mainly locking in the timezone behavior we verified by hand while building
this: Flight.departure and Flight.arrival must be real timezone-aware
datetimes, and subtracting them must give the correct elapsed flight time
even when origin and destination are in different timezones and on
different calendar dates.
"""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from converge.airports import AIRPORTS
from converge.models import Flight


def test_flight_departure_and_arrival_are_timezone_aware():
    origin_tz = ZoneInfo(AIRPORTS["JFK"]["timezone"])
    dest_tz = ZoneInfo(AIRPORTS["NRT"]["timezone"])

    departure = datetime(2026, 10, 1, 13, 30, tzinfo=origin_tz)
    arrival = departure.astimezone(ZoneInfo("UTC")) + timedelta(hours=14)
    arrival = arrival.astimezone(dest_tz)

    flight = Flight(origin="JFK", destination="NRT", departure=departure, arrival=arrival, price_usd=850)

    assert flight.departure.tzinfo is not None
    assert flight.arrival.tzinfo is not None


def test_flight_duration_correct_across_timezones_and_dates():
    """The whole point of timezone-aware datetimes: elapsed time comes out
    right even though departure and arrival are in different timezones and
    land on different calendar dates."""
    origin_tz = ZoneInfo(AIRPORTS["JFK"]["timezone"])
    dest_tz = ZoneInfo(AIRPORTS["NRT"]["timezone"])

    departure = datetime(2026, 10, 1, 13, 30, tzinfo=origin_tz)
    arrival = departure.astimezone(ZoneInfo("UTC")) + timedelta(hours=14)
    arrival = arrival.astimezone(dest_tz)

    flight = Flight(origin="JFK", destination="NRT", departure=departure, arrival=arrival, price_usd=850)

    assert flight.arrival.date() != flight.departure.date()
    assert flight.arrival - flight.departure == timedelta(hours=14)