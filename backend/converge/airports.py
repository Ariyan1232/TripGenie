"""
A tiny reference table of airports we know about.

Each airport needs an IANA timezone name (e.g. "America/New_York") so that
when a Flight has a departure/arrival time, we know what timezone that time
is actually in. This list is deliberately small -- just enough to build and
test against, not a real airport database. It'll likely grow into something
with real lat/lon for distance calculations once we need that.
"""

AIRPORTS = {
    "JFK": {"city": "New York", "timezone": "America/New_York"},
    "LHR": {"city": "London", "timezone": "Europe/London"},
    "NRT": {"city": "Tokyo", "timezone": "Asia/Tokyo"},
}