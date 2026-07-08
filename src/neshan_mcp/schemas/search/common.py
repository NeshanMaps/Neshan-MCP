"""Shared schema pieces for the search domain."""

from __future__ import annotations

from pydantic import BaseModel

from ..shared import Latitude, Longitude


class LatLng(BaseModel):
    lat: Latitude
    lng: Longitude
