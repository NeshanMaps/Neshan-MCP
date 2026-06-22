"""Coordinate formatting helpers (Neshan uses "lat,lng")."""

from __future__ import annotations

from collections.abc import Sequence


def coord(lat: float, lng: float) -> str:
    return f"{lat},{lng}"


def coord_list(points: Sequence[Sequence[float]]) -> str:
    """Join [[lat, lng], ...] into Neshan's "lat,lng|lat,lng" form."""
    return "|".join(f"{p[0]},{p[1]}" for p in points)
