"""Input schema for the traffic analytics domain."""

from __future__ import annotations

from pydantic import BaseModel, Field

from ..shared import Latitude, Longitude


class TrafficAnalyticsInput(BaseModel):
    lat: Latitude = Field(description="Latitude of the location.")
    lng: Longitude = Field(description="Longitude of the location.")
