"""Input schemas for the routing domain (direction, matrix, tsp, map matching)."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, model_validator

from ..shared import validate_pairs
from .common import Vehicle


class DirectionInput(BaseModel):
    origin_lat: float = Field(ge=-90, le=90)
    origin_lng: float = Field(ge=-180, le=180)
    dest_lat: float = Field(ge=-90, le=90)
    dest_lng: float = Field(ge=-180, le=180)
    vehicle: Vehicle = "car"
    waypoints: list[list[float]] | None = None
    avoid_traffic_zone: bool = False
    avoid_odd_even_zone: bool = False
    alternative: bool = False
    bearing: int | None = Field(default=None, ge=0, le=360)

    @field_validator("waypoints")
    @classmethod
    def _check_waypoints(cls, v):
        if v:
            return validate_pairs(v, field="waypoints", minimum=1)
        return v


class MatrixInput(BaseModel):
    origins: list[list[float]]
    destinations: list[list[float]]

    @field_validator("origins")
    @classmethod
    def _v_origins(cls, v):
        return validate_pairs(v, field="origins", minimum=1)

    @field_validator("destinations")
    @classmethod
    def _v_destinations(cls, v):
        return validate_pairs(v, field="destinations", minimum=1)


class TspInput(BaseModel):
    waypoints: list[list[float]]
    round_trip: bool = True
    source_is_any_point: bool = False
    last_is_any_point: bool = False

    @field_validator("waypoints")
    @classmethod
    def _v_waypoints(cls, v):
        return validate_pairs(v, field="waypoints", minimum=2)


class MapMatchingInput(BaseModel):
    path_points: list[list[float]]

    @field_validator("path_points")
    @classmethod
    def _v_points(cls, v):
        return validate_pairs(v, field="path_points", minimum=2)


class IsochroneInput(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    distance: float | None = Field(default=None, gt=0)
    time: float | None = Field(default=None, gt=0)
    polygon: bool = False
    denoise: float = Field(default=0.0, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def _require_distance_or_time(self) -> "IsochroneInput":
        if self.distance is None and self.time is None:
            raise ValueError("At least one of 'distance' or 'time' must be provided.")
        return self
