"""MCP tool definitions for the map domain."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from .. import handlers
from ..schemas.shared import Latitude, Longitude
from ..services import NeshanClient


def register(mcp, client: NeshanClient) -> None:
    @mcp.tool
    async def neshan_static_map(
        lat: Latitude, lng: Longitude,
        zoom: Annotated[int, Field(ge=1, le=20)] = 15,
        width: Annotated[int, Field(ge=16, le=2048)] = 500,
        height: Annotated[int, Field(ge=16, le=2048)] = 500,
        map_type: str = "light", marker: str | None = "red",
    ):
        """Render a static map image (PNG) centered on a coordinate.

        Args:
            lat, lng: Center of the map.
            zoom: Zoom level (1-20).
            width, height: Image size in pixels (16-2048).
            map_type: Style, e.g. 'light', 'dark', 'standard-night'.
            marker: Marker color at the center (e.g. 'red'), or None.
        """
        return await handlers.handle_static_map(
            client, lat=lat, lng=lng, zoom=zoom, width=width, height=height,
            map_type=map_type, marker=marker,
        )

    @mcp.tool
    async def neshan_static_map_arc(
        origin_lat: Latitude, origin_lng: Longitude,
        dest_lat: Latitude, dest_lng: Longitude,
        width: Annotated[int, Field(ge=16, le=2000)] = 600,
        height: Annotated[int, Field(ge=16, le=1200)] = 600,
        map_type: str = "standard-night",
        dashed: bool = False,
        color: str | None = None,
        marker1_token: str | None = None,
        marker2_token: str | None = None,
    ):
        """Render a static map image (PNG) with a curved arc line between two points.

        Useful for visualising geographic connections, travel reports, or origin-destination
        relationships on a map without performing full routing.

        Args:
            origin_lat, origin_lng: Arc start point.
            dest_lat, dest_lng: Arc end point.
            width: Image width in pixels (16-2000).
            height: Image height in pixels (16-1200).
            map_type: Map style — 'standard-night' or 'dreamy'.
            dashed: Render the arc as a dashed line.
            color: Arc colour as a hex string (e.g. '#FF0AA5'). Defaults to API default.
            marker1_token: Custom icon token for the origin marker (upload via Neshan panel).
            marker2_token: Custom icon token for the destination marker.
        """
        return await handlers.handle_static_map_arc(
            client,
            origin_lat=origin_lat, origin_lng=origin_lng,
            dest_lat=dest_lat, dest_lng=dest_lng,
            width=width, height=height,
            map_type=map_type, dashed=dashed,
            color=color,
            marker1_token=marker1_token, marker2_token=marker2_token,
        )
