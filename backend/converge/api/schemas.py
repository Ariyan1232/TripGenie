"""
API request and response schemas.

These are separate from the internal converge models on purpose --
the API's input/output shape can change without touching the solver,
and the solver's internal models can change without breaking the API.
"""

from datetime import date
from pydantic import BaseModel


# ---- Requests (what the client sends) ----

class TravelerIn(BaseModel):
    name: str
    origin_airport: str        # IATA code, e.g. "JFK"
    earliest_departure: date
    latest_return: date
    destination_votes: list[str] = []


class CreateTripIn(BaseModel):
    name: str
    organizer_name: str
    organizer_origin: str
    organizer_earliest: date
    organizer_latest: date
    organizer_votes: list[str] = []


# ---- Responses (what the API sends back) ----

class TravelerOut(BaseModel):
    id: str
    name: str
    origin_airport: str
    earliest_departure: date
    latest_return: date
    destination_votes: list[str]


class TripOut(BaseModel):
    id: str
    name: str
    travelers: list[TravelerOut]


class FlightOut(BaseModel):
    origin: str
    destination: str
    departure: str   # formatted string, e.g. "Oct 13 14:00 EDT"
    arrival: str     # formatted string, e.g. "Oct 14 06:30 JST"
    price_usd: float


class SolverResultOut(BaseModel):
    label: str
    spread_hours: float
    total_cost: float
    flights: list[FlightOut]


class DestinationResultOut(BaseModel):
    destination: str
    city_name: str
    vote_count: int
    options: list[SolverResultOut]


class ResultsOut(BaseModel):
    trip_id: str
    destinations: list[DestinationResultOut]