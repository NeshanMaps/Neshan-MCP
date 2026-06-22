"""Input schemas for the search domain (search, reverse, geocode)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, model_validator

from .common import LatLng


class SearchInput(LatLng):
    term: str = Field(min_length=1)


class ReverseInput(LatLng):
    pass


class GeocodeInput(BaseModel):
    address: str = Field(min_length=1)


class GeocodePlusInput(BaseModel):
    address: str = Field(min_length=1)
    city: str | None = None
    province: str | None = None
    bias_lat: float | None = Field(default=None, ge=-90, le=90)
    bias_lng: float | None = Field(default=None, ge=-180, le=180)
    sw_lat: float | None = Field(default=None, ge=-90, le=90)
    sw_lng: float | None = Field(default=None, ge=-180, le=180)
    ne_lat: float | None = Field(default=None, ge=-90, le=90)
    ne_lng: float | None = Field(default=None, ge=-180, le=180)

    @model_validator(mode="after")
    def _check_pairs(self):
        if (self.bias_lat is None) != (self.bias_lng is None):
            raise ValueError("bias_lat and bias_lng must be provided together")
        extent = (self.sw_lat, self.sw_lng, self.ne_lat, self.ne_lng)
        if any(v is not None for v in extent) and any(v is None for v in extent):
            raise ValueError("extent requires sw_lat, sw_lng, ne_lat, ne_lng together")
        return self

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"address": self.address}
        if self.city:
            payload["city"] = self.city
        if self.province:
            payload["province"] = self.province
        if self.bias_lat is not None and self.bias_lng is not None:
            payload["location"] = {"latitude": self.bias_lat, "longitude": self.bias_lng}
        if self.sw_lat is not None:
            payload["extent"] = {
                "southWest": {"latitude": self.sw_lat, "longitude": self.sw_lng},
                "northEast": {"latitude": self.ne_lat, "longitude": self.ne_lng},
            }
        return payload
