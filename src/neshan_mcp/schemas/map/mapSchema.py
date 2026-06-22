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
