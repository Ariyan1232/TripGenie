from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class Traveler:
    id: str
    name: str
    origin_airport: str
    earliest_departure: date
    latest_return: date
    destination_votes: list[str] = field(default_factory=list)


@dataclass
class Flight:
    origin: str
    destination: str
    departure: datetime
    arrival: datetime
    price_usd: float


@dataclass
class SolverResult:
    label: str
    flights: list[Flight]
    spread_hours: float
    total_cost: float


@dataclass
class DestinationResult:
    """
    The solver's findings for one candidate destination --
    all three labeled options plus the destination itself,
    so the group can compare across destinations.
    """
    destination: str
    city_name: str
    vote_count: int
    options: list[SolverResult]

    @property
    def best_synced(self) -> SolverResult:
        return next(r for r in self.options if r.label == "Best synced")

    @property
    def cheapest(self) -> SolverResult:
        return next(r for r in self.options if r.label == "Cheapest")