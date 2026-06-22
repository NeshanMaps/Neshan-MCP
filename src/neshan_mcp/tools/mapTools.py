"""MCP tool definitions for the map domain."""

from __future__ import annotations

from .. import handlers
from ..services import NeshanClient


def register(mcp, client: NeshanClient) -> None:
    @mcp.tool
    async def neshan_static_map(
        lat: float, lng: float, zoom: int = 15, width: int = 500, height: int = 500,
        map_type: str = "light", marker: str | None = "red",
    ):
        """Render a static map image (PNG) centered on a coordinate.

        Args:
            lat, lng: Center of the map.
            zoom: Zoom level (1-20).
            width, height: Image size in pixels.
            map_type: Style, e.g. 'light', 'dark', 'standard-night'.
            marker: Marker color at the center (e.g. 'red'), or None.
        """
        return await handlers.handle_static_map(
            client, lat=lat, lng=lng, zoom=zoom, width=width, height=height,
            map_type=map_type, marker=marker,
        )
