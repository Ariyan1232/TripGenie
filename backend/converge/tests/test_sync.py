"""
Tests for sync.py.

The key test here is test_gap_correct_across_different_origin_timezones --
it confirms that two people departing from different timezones but landing
at the exact same absolute moment correctly produce a gap of 0, not the
difference between their local departure times (which would be wrong).
"""

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from converge.models import Flight
from converge.sync import arrival_gap_hours


def make_flight(origin_tz_name, dest_tz_name, dep_hour, duration_hours):
    """Helper: build a Flight with a specific departure hour and duration."""
    origin_tz = ZoneInfo(origin_tz_name)
    dest_tz = ZoneInfo(dest_tz_name)
    departure = datetime(2026, 10, 1, dep_hour, 0, tzinfo=origin_tz)
    arrival_utc = departure.astimezone(ZoneInfo("UTC")) + timedelta(hours=duration_hours)
    arrival = arrival_utc.astimezone(dest_tz)
    return Flight(origin="???", destination="???", departure=departure, arrival=arrival, price_usd=0)


def test_gap_is_zero_when_arrivals_are_identical():
    f = make_flight("America/New_York", "Asia/Tokyo", dep_hour=10, duration_hours=14)
    assert arrival_gap_hours(f, f) == 0.0


def test_gap_is_correct_for_known_difference():
    """Two flights to Tokyo, one arriving exactly 3 hours after the other."""
    f1 = make_flight("America/New_York", "Asia/Tokyo", dep_hour=10, duration_hours=14)
    f2 = make_flight("America/New_York", "Asia/Tokyo", dep_hour=13, duration_hours=14)
    assert abs(arrival_gap_hours(f1, f2) - 3.0) < 0.01


def test_gap_is_symmetric():
    """Gap from A to B should equal gap from B to A."""
    f1 = make_flight("America/New_York", "Asia/Tokyo", dep_hour=10, duration_hours=14)
    f2 = make_flight("Europe/London", "Asia/Tokyo", dep_hour=20, duration_hours=12)
    assert arrival_gap_hours(f1, f2) == arrival_gap_hours(f2, f1)


def test_gap_correct_across_different_origin_timezones():
    """
    The key test: two people landing at the same absolute moment but
    departing from different timezones. Gap should be 0, not the
    difference between their local departure times.
    """
    dest_tz = ZoneInfo("Asia/Tokyo")
    utc = ZoneInfo("UTC")

    shared_arrival_utc = datetime(2026, 10, 2, 6, 0, tzinfo=utc)

    f1 = Flight(
        origin="JFK", destination="NRT",
        departure=datetime(2026, 10, 1, 10, 0, tzinfo=ZoneInfo("America/New_York")),
        arrival=shared_arrival_utc.astimezone(dest_tz),
        price_usd=900,
    )
    f2 = Flight(
        origin="LHR", destination="NRT",
        departure=datetime(2026, 10, 1, 18, 0, tzinfo=ZoneInfo("Europe/London")),
        arrival=shared_arrival_utc.astimezone(dest_tz),
        price_usd=700,
    )

    assert arrival_gap_hours(f1, f2) == 0.0