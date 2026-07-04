"""MCP tool definitions for the traffic analytics domain."""

from __future__ import annotations

from .. import handlers
from ..schemas.shared import Latitude, Longitude
from ..services import NeshanClient


def register(mcp, client: NeshanClient) -> None:
    @mcp.tool
    async def neshan_traffic_analytics(lat: Latitude, lng: Longitude):
        """Analyse historical traffic patterns around a location.

        Returns three things:
        - **kpi**: overall traffic congestion score for the location (higher = more congested).
        - **chart**: 24-hour traffic breakdown — one entry per hour with a numeric score and
          a color key (green → free flow, yellow → moderate, orange → heavy, red → congested).
        - **static_map**: a PNG image of the area (~500 m radius) with traffic overlay.

        Args:
            lat: Latitude of the location.
            lng: Longitude of the location.
        """
        return await handlers.handle_traffic_analytics(client, lat=lat, lng=lng)
