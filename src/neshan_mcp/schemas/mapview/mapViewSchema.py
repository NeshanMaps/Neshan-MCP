"""Input schemas for the interactive map view tool."""

from __future__ import annotations

from pydantic import BaseModel, Field

from ..shared import Latitude, Longitude


class MarkerInput(BaseModel):
    lat: Latitude
    lng: Longitude
    label: str = Field(default="", description="Popup text shown when the marker is clicked.")
    color: str = Field(default="#E53935", description="Marker color as a CSS color (hex, e.g. '#E53935').")


class RouteInput(BaseModel):
    """یه مسیر کدشده با polyline یا لیست نقاط."""
    encoded_polyline: str | None = Field(
        default=None,
        description="Encoded polyline to draw, e.g. the 'overview_polyline' field from "
                    "neshan_direction. Takes precedence over 'coordinates' if both are given.",
    )
    coordinates: list[list[float]] | None = Field(
        default=None,
        description="Raw route points as [[lat, lng], ...]; used only if 'encoded_polyline' is not given.",
    )
    color: str = Field(default="#1565C0", description="Line color as a CSS color (hex, e.g. '#1565C0').")
    label: str = Field(default="", description="Label shown on the route layer.")


class MapViewInput(BaseModel):
    center_lat: Latitude = 35.6892
    center_lng: Longitude = 51.389
    zoom: int = Field(default=12, ge=2, le=21)
    markers: list[MarkerInput] = Field(default_factory=list)
    routes: list[RouteInput] = Field(default_factory=list)
    title: str = "نقشه نشان"
    show_traffic: bool = False
    show_poi: bool = True
    map_key: str = ""   # web map api key — جدا از service key
