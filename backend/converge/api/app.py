"""
Converge REST API.

Four endpoints covering the full user flow:

  POST /trips                      create a trip
  GET  /trips/{trip_id}            get trip details
  POST /trips/{trip_id}/travelers  add a traveler
  GET  /trips/{trip_id}/results    run the solver, get ranked destinations

State is in-memory for now (a plain dict). This means data is lost
when the server restarts -- that's fine while we're validating the
product. Swapping in a real database later only touches this file,
not the solver or voting logic.
"""

import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ..models import Traveler
from ..voting import compare_destinations
from .schemas import (
    CreateTripIn,
    TravelerIn,
    TripOut,
    TravelerOut,
    ResultsOut,
    DestinationResultOut,
    SolverResultOut,
    FlightOut,
)

app = FastAPI(title="Converge API", version="0.1.0")

# Allow the frontend (running on a different port) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store: trip_id -> {"name": str, "travelers": list[Traveler]}
trips: dict[str, dict] = {}


# ---- Helpers ----

def _traveler_out(t: Traveler) -> TravelerOut:
    return TravelerOut(
        id=t.id,
        name=t.name,
        origin_airport=t.origin_airport,
        earliest_departure=t.earliest_departure,
        latest_return=t.latest_return,
        destination_votes=t.destination_votes,
    )


def _format_dt(dt) -> str:
    return dt.strftime("%b %d %H:%M %Z")


# ---- Endpoints ----

@app.post("/trips", response_model=TripOut, status_code=201)
def create_trip(body: CreateTripIn):
    """Create a new trip. The organizer is added as the first traveler."""
    trip_id = str(uuid.uuid4())[:8]
    organizer = Traveler(
        id=str(uuid.uuid4())[:8],
        name=body.organizer_name,
        origin_airport=body.organizer_origin,
        earliest_departure=body.organizer_earliest,
        latest_return=body.organizer_latest,
        destination_votes=body.organizer_votes,
    )
    trips[trip_id] = {"name": body.name, "travelers": [organizer]}
    return TripOut(
        id=trip_id,
        name=body.name,
        travelers=[_traveler_out(organizer)],
    )


@app.get("/trips/{trip_id}", response_model=TripOut)
def get_trip(trip_id: str):
    """Get trip details and current traveler list."""
    trip = trips.get(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return TripOut(
        id=trip_id,
        name=trip["name"],
        travelers=[_traveler_out(t) for t in trip["travelers"]],
    )


@app.post("/trips/{trip_id}/travelers", response_model=TripOut, status_code=201)
def add_traveler(trip_id: str, body: TravelerIn):
    """Add a traveler to an existing trip."""
    trip = trips.get(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    traveler = Traveler(
        id=str(uuid.uuid4())[:8],
        name=body.name,
        origin_airport=body.origin_airport,
        earliest_departure=body.earliest_departure,
        latest_return=body.latest_return,
        destination_votes=body.destination_votes,
    )
    trip["travelers"].append(traveler)

    return TripOut(
        id=trip_id,
        name=trip["name"],
        travelers=[_traveler_out(t) for t in trip["travelers"]],
    )


@app.get("/trips/{trip_id}/results", response_model=ResultsOut)
def get_results(trip_id: str):
    """
    Run the solver across all agreed destinations and return
    ranked results. This is the core endpoint -- it calls into
    voting.compare_destinations() which runs the full pipeline:
    agreed destinations -> date search -> solver -> ranked output.
    """
    trip = trips.get(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    travelers = trip["travelers"]
    if len(travelers) < 2:
        raise HTTPException(
            status_code=400,
            detail="Need at least 2 travelers to compare destinations",
        )

    dest_results = compare_destinations(travelers)

    if not dest_results:
        raise HTTPException(
            status_code=400,
            detail="No destinations that all travelers agreed on, "
                   "or no overlapping availability window found",
        )

    destinations_out = []
    for dr in dest_results:
        options_out = []
        for sr in dr.options:
            flights_out = [
                FlightOut(
                    origin=f.origin,
                    destination=f.destination,
                    departure=_format_dt(f.departure),
                    arrival=_format_dt(f.arrival),
                    price_usd=f.price_usd,
                )
                for f in sr.flights
            ]
            options_out.append(SolverResultOut(
                label=sr.label,
                spread_hours=round(sr.spread_hours, 2),
                total_cost=round(sr.total_cost, 2),
                flights=flights_out,
            ))
        destinations_out.append(DestinationResultOut(
            destination=dr.destination,
            city_name=dr.city_name,
            vote_count=dr.vote_count,
            options=options_out,
        ))

    return ResultsOut(trip_id=trip_id, destinations=destinations_out)