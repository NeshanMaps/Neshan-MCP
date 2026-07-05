"""MCP tool definitions for utility functions (deeplinks)."""

from __future__ import annotations

from typing import Literal

from ..schemas.shared import Latitude, Longitude
from ..utils.deeplinks import point_links, routing_links


def register(mcp, _client) -> None:
    @mcp.tool
    async def neshan_deeplink(
        link_type: Literal["point", "routing"],
        lat: Latitude | None = None,
        lng: Longitude | None = None,
        origin_lat: Latitude | None = None,
        origin_lng: Longitude | None = None,
        dest_lat: Latitude | None = None,
        dest_lng: Longitude | None = None,
        vehicle: Literal["car", "motorcycle", "pedestrian", "bicycle", "transit"] = "car",
    ) -> dict:
        """Generate Neshan app deeplinks for showing a point or navigating between two points.

        If the Neshan app is installed the link opens it directly; otherwise it falls back
        to the Neshan web app. Returns both Android/Web and iOS variants.

        Args:
            link_type: 'point' to pin a location, 'routing' for turn-by-turn navigation.
            lat, lng: Required when link_type='point'.
            origin_lat, origin_lng: Route start — required when link_type='routing'.
            dest_lat, dest_lng: Route end — required when link_type='routing'.
            vehicle: 'car' (default), 'motorcycle', 'pedestrian', 'bicycle', 'transit'.
                     Note: Android/Web only supports 'car' and 'motorcycle'.
        """
        if link_type == "point":
            if lat is None or lng is None:
                raise ValueError("lat and lng are required for link_type='point'")
            return point_links(lat, lng)
        if any(v is None for v in (origin_lat, origin_lng, dest_lat, dest_lng)):
            raise ValueError(
                "origin_lat, origin_lng, dest_lat, dest_lng are required for link_type='routing'"
            )
        return routing_links(origin_lat, origin_lng, dest_lat, dest_lng, vehicle)
