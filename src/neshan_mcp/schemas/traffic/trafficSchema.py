"""Input schema for the traffic analytics domain."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TrafficAnalyticsInput(BaseModel):
    lat: float = Field(ge=-90, le=90, description="Latitude of the location.")
    lng: float = Field(ge=-180, le=180, description="Longitude of the location.")
