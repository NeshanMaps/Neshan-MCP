"""Handlers for the point domain."""

from __future__ import annotations

import math
from typing import Any

from ..schemas.point import PointInput
from ..services import NeshanClient, pointService
from ..utils import handle_api_errors, point_links

_HALF_CIRCUMFERENCE = 20037508.342789244


def _mercator_to_wgs84(x: float, y: float) -> tuple[float, float]:
    """Convert Web Mercator (EPSG:3857) metres to WGS84 decimal degrees."""
    lng = x / _HALF_CIRCUMFERENCE * 180.0
    lat = math.degrees(2.0 * math.atan(math.exp(y / _HALF_CIRCUMFERENCE * math.pi)) - math.pi / 2.0)
    return lat, lng


@handle_api_errors
async def handle_get_point(client: NeshanClient, hash: str) -> dict[str, Any]:
    result = await pointService.get_point(client, PointInput(hash=hash))
    loc = result.get("location") or {}
    mx, my = loc.get("x"), loc.get("y")
    if mx is not None and my is not None:
        lat, lng = _mercator_to_wgs84(mx, my)
        result["neshan_links"] = point_links(lat, lng)
    return result
