"""Input schemas for the interactive map view tool."""

from __future__ import annotations

from pydantic import BaseModel, Field

from ..shared import Latitude, Longitude


class MarkerInput(BaseModel):
    lat: Latitude
    lng: Longitude
    label: str = ""
    color: str = "#E53935"  # قرمز پیش‌فرض


class RouteInput(BaseModel):
    """یه مسیر کدشده با polyline یا لیست نقاط."""
    encoded_polyline: str | None = None          # overview_polyline از direction
    coordinates: list[list[float]] | None = None  # [[lat,lng],...]
    color: str = "#1565C0"
    label: str = ""


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
