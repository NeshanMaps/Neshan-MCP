"""Shared schema validators."""

from __future__ import annotations

from collections.abc import Sequence


def validate_pairs(points: Sequence[Sequence[float]], *, field: str, minimum: int = 1):
    """Validate a list of [lat, lng] pairs; raise ValueError on bad input."""
    if not points or len(points) < minimum:
        raise ValueError(f"{field}: at least {minimum} point(s) required")
    for i, p in enumerate(points):
        if len(p) != 2:
            raise ValueError(f"{field}[{i}]: expected [lat, lng]")
        lat, lng = p
        if not (-90 <= lat <= 90):
            raise ValueError(f"{field}[{i}].lat out of range: {lat}")
        if not (-180 <= lng <= 180):
            raise ValueError(f"{field}[{i}].lng out of range: {lng}")
    return points
