"""Input schema for the map domain (static map)."""

from __future__ import annotations

from pydantic import BaseModel, Field

from ..shared import Latitude, Longitude


class StaticMapInput(BaseModel):
    lat: Latitude
    lng: Longitude
    zoom: int = Field(default=15, ge=1, le=20)
    width: int = Field(default=500, ge=16, le=2048)
    height: int = Field(default=500, ge=16, le=2048)
    map_type: str = "light"
    marker: str | None = "red"


class StaticMapArcInput(BaseModel):
    origin_lat: Latitude
    origin_lng: Longitude
    dest_lat: Latitude
    dest_lng: Longitude
    width: int = Field(default=600, ge=16, le=2000)
    height: int = Field(default=600, ge=16, le=1200)
    map_type: str = "standard-night"
    dashed: bool = False
    color: str | None = None
    marker1_token: str | None = None
    marker2_token: str | None = None
