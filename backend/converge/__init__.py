"""
converge -- multi-origin flight convergence solver (early build).

Public API so far:

    from converge import Traveler, Flight, AIRPORTS

This will grow as we add more pieces (mock flight search, the solver
itself, trip/expense tracking). See README.md at the project root for
where we are and what's intentionally not built yet.
"""

from .airports import AIRPORTS
from .models import Flight, Traveler

__all__ = [
    "AIRPORTS",
    "Flight",
    "Traveler",
]