"""
Distance calculations between airports.

Uses the haversine formula to compute great-circle distance -- the
shortest path between two points along the surface of a sphere. This
matters because naive "subtract the lat/lon values" math badly distorts
distance for long east-west routes (it doesn't account for the Earth's
curvature, and gets worse the further you are from the equator).
"""

import math

from .airports import AIRPORTS

EARTH_RADIUS_KM = 6371.0


def distance_km(origin: str, destination: str) -> float:
    """Great-circle distance between two airports, in kilometers."""
    lat1, lon1 = AIRPORTS[origin]["lat"], AIRPORTS[origin]["lon"]
    lat2, lon2 = AIRPORTS[destination]["lat"], AIRPORTS[destination]["lon"]

    # Convert degrees to radians, since the math functions expect radians.
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_KM * c