"""Input schemas for the VRP (Vehicle Routing Problem) logistic domain."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class VRPTimeWindow(BaseModel):
    from_time: str = Field(alias="from", description="Start time, e.g. '06:00:00'.")
    to: str = Field(description="End time, e.g. '18:00:00'.")

    model_config = {"populate_by_name": True}


class VRPLocation(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class VRPVehicle(BaseModel):
    id: int | str
    capacity: int = Field(ge=0)
    skills: list[int] = Field(default_factory=list)
    timeWindow: VRPTimeWindow
    startLocation: VRPLocation | None = None
    endLocation: VRPLocation | None = None


class VRPJob(BaseModel):
    id: int | str
    location: VRPLocation
    setUpTime: int = Field(default=0, ge=0, description="Setup time in seconds.")
    serviceTime: int = Field(default=0, ge=0, description="Service time in seconds.")
    delivery: int = Field(default=0, ge=0)
    pickup: int = Field(default=0, ge=0)
    priority: int = Field(default=1, ge=1)
    skills: list[int] = Field(default_factory=list)
    timeWindows: list[VRPTimeWindow] = Field(default_factory=list)


class VRPInput(BaseModel):
    vehicles: list[VRPVehicle]
    jobs: list[VRPJob]
    depot: VRPLocation
    planTime: int = Field(
        default=45000,
        ge=1000,
        description="Max planning time in milliseconds.",
    )
    solutionStrategy: Literal["BEST_EFFORT", "FAST", "THOROUGH"] = "BEST_EFFORT"
    costType: Literal["DISTANCE", "DURATION"] = "DISTANCE"
    explorationLevel: Literal["LOW", "MEDIUM", "HIGH"] = "MEDIUM"
    routingEngine: Literal["typical", "car", "motorcycle"] = "typical"
    balanceWorkload: bool = False
    useTimeBalancing: bool = False
    useTrafficMultiplier: bool = False
