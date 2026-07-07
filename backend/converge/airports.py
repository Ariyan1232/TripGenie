"""
A tiny reference table of airports we know about.

Each airport needs:
- an IANA timezone name (e.g. "America/New_York"), so a Flight's
  departure/arrival times can be correctly anchored to the right timezone
- a latitude/longitude, so we can compute real distances between airports
  (which then drives realistic flight price/duration)

This list is deliberately small -- just enough to build and test against,
not a real airport database.
"""

AIRPORTS = {
    "JFK": {"city": "New York",    "timezone": "America/New_York",   "lat": 40.6413, "lon": -73.7781},
    "LHR": {"city": "London",      "timezone": "Europe/London",       "lat": 51.4700, "lon":  -0.4543},
    "NRT": {"city": "Tokyo",       "timezone": "Asia/Tokyo",          "lat": 35.7720, "lon": 140.3929},
    "CDG": {"city": "Paris",       "timezone": "Europe/Paris",        "lat": 49.0097, "lon":   2.5479},
    "BKK": {"city": "Bangkok",     "timezone": "Asia/Bangkok",        "lat": 13.6811, "lon": 100.7472},
    "SIN": {"city": "Singapore",   "timezone": "Asia/Singapore",      "lat":  1.3644, "lon": 103.9915},
    "LAX": {"city": "Los Angeles", "timezone": "America/Los_Angeles", "lat": 33.9425, "lon":-118.4081},
    "DXB": {"city": "Dubai",       "timezone": "Asia/Dubai",          "lat": 25.2532, "lon":  55.3657},
}