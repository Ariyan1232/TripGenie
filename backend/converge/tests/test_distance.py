"""
Tests for distance.py.

Confirms the haversine distance calculation gives sane, real-world-accurate
results -- this matters because an earlier, naive approach (just
subtracting lat/lon values directly) badly distorted long-haul routes.
"""

from converge.distance import distance_km


def test_distance_is_realistic_for_known_routes():
    # Real-world approx distances, with generous tolerance since this is a
    # simplified spherical-Earth model, not survey-grade geodesy.
    assert 5300 < distance_km("JFK", "LHR") < 5800
    assert 10500 < distance_km("JFK", "NRT") < 11200
    assert 9200 < distance_km("LHR", "NRT") < 9900


def test_longer_routes_are_actually_longer():
    """Sanity check on relative ordering, not just absolute numbers --
    this is the kind of check that would have caught the original bug,
    where a transatlantic route was miscalculated as longer than a
    transpacific one."""
    jfk_lhr = distance_km("JFK", "LHR")
    jfk_nrt = distance_km("JFK", "NRT")
    assert jfk_nrt > jfk_lhr


def test_distance_is_symmetric():
    """Distance from A to B should equal distance from B to A."""
    assert abs(distance_km("JFK", "NRT") - distance_km("NRT", "JFK")) < 0.01