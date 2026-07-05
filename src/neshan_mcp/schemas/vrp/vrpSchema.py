"""Input schemas for the VRP (Vehicle Routing Problem) logistic domain."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from ..shared import Latitude, Longitude


class VRPTimeWindow(BaseModel):
    from_time: str = Field(alias="from", description="Start time, e.g. '06:00:00'.")
    to: str = Field(description="End time, e.g. '18:00:00'.")

    model_config = {"populate_by_name": True}


class VRPLocation(BaseModel):
    latitude: Latitude
    longitude: Longitude


class VRPVehicle(BaseModel):
    id: int | str = Field(description="Unique vehicle identifier; echoed back in the route results.")
    capacity: int = Field(ge=0, description="Max total delivery+pickup load the vehicle can carry.")
    skills: list[int] = Field(
        default_factory=list,
        description="Arbitrary skill-tag IDs this vehicle has. A job is only assignable to this "
                    "vehicle if all of the job's 'skills' are present here.",
    )
    timeWindow: VRPTimeWindow = Field(description="When this vehicle is available to operate.")
    startLocation: VRPLocation | None = Field(
        default=None, description="Where this vehicle starts its route. Defaults to the shared 'depot'.",
    )
    endLocation: VRPLocation | None = Field(
        default=None, description="Where this vehicle's route must end. Defaults to the shared 'depot'.",
    )


class VRPJob(BaseModel):
    id: int | str = Field(description="Unique job identifier; echoed back in the route results.")
    location: VRPLocation = Field(description="Where this job must be performed.")
    setUpTime: int = Field(default=0, ge=0, description="Setup time in seconds.")
    serviceTime: int = Field(default=0, ge=0, description="Service time in seconds.")
    delivery: int = Field(default=0, ge=0, description="Load amount dropped off at this job (same unit as vehicle capacity).")
    pickup: int = Field(default=0, ge=0, description="Load amount picked up at this job (same unit as vehicle capacity).")
    priority: int = Field(default=1, ge=1, description="Relative scheduling priority versus other jobs when not all can be fit (see platform.neshan.org docs for the exact ordering convention).")
    skills: list[int] = Field(
        default_factory=list,
        description="Skill-tag IDs required to perform this job. Must be a subset of the "
                    "assigned vehicle's 'skills'.",
    )
    timeWindows: list[VRPTimeWindow] = Field(
        default_factory=list, description="Allowed time window(s) for performing this job.",
    )


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
