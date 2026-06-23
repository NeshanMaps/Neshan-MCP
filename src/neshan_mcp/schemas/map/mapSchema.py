"""Input schema for the map domain (static map)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class StaticMapInput(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    zoom: int = Field(default=15, ge=1, le=20)
    width: int = Field(default=500, ge=16, le=2048)
    height: int = Field(default=500, ge=16, le=2048)
    map_type: str = "light"
    marker: str | None = "red"


class StaticMapArcInput(BaseModel):
    origin_lat: float = Field(ge=-90, le=90)
    origin_lng: float = Field(ge=-180, le=180)
    dest_lat: float = Field(ge=-90, le=90)
    dest_lng: float = Field(ge=-180, le=180)
    width: int = Field(default=600, ge=16, le=2000)
    height: int = Field(default=600, ge=16, le=1200)
    map_type: str = "standard-night"
    dashed: bool = False
    color: str | None = None
    marker1_token: str | None = None
    marker2_token: str | None = None
