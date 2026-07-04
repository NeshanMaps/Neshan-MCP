"""Input schemas for the interactive map view tool."""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class MarkerInput(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    label: str = ""
    color: str = "#E53935"  # قرمز پیش‌فرض


class RouteInput(BaseModel):
    """یه مسیر کدشده با polyline یا لیست نقاط."""
    encoded_polyline: str | None = None          # overview_polyline از direction
    coordinates: list[list[float]] | None = None  # [[lat,lng],...]
    color: str = "#1565C0"
    label: str = ""


class MapViewInput(BaseModel):
    center_lat: float = Field(default=35.6892, ge=-90, le=90)
    center_lng: float = Field(default=51.389, ge=-180, le=180)
    zoom: int = Field(default=12, ge=2, le=21)
    markers: list[MarkerInput] = Field(default_factory=list)
    routes: list[RouteInput] = Field(default_factory=list)
    title: str = "نقشه نشان"
    show_traffic: bool = False
    show_poi: bool = True
    map_key: str = ""   # web map api key — جدا از service key
