"""MCP tool definition for the interactive map view."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from .. import handlers
from ..schemas.mapview import MarkerInput, RouteInput
from ..schemas.shared import Latitude, Longitude
from ..services import NeshanClient


def register(mcp, client: NeshanClient) -> None:
    @mcp.tool
    async def neshan_map_view(
        title: str = "نقشه نشان",
        center_lat: Latitude = 35.6892,
        center_lng: Longitude = 51.389,
        zoom: Annotated[int, Field(ge=2, le=21)] = 12,
        markers: list[MarkerInput] | None = None,
        routes: list[RouteInput] | None = None,
        show_traffic: bool = False,
        show_poi: bool = True,
        map_key: str = "",
    ):
        """Generate an interactive Neshan map HTML file and save it locally.

        Creates a fully interactive map page using the Neshan Maps SDK.
        Supports markers with popups and route polylines drawn on the map.
        The map auto-fits to show all markers and routes.
        Open the returned file_path in any browser to view the map.

        Args:
            title: Page title shown in the header bar.
            center_lat: Fallback center latitude (used when no markers/routes given).
            center_lng: Fallback center longitude.
            zoom: Initial zoom level (2–21). Auto-calculated when markers/routes are present.
            markers: Marker objects to place on the map.
            routes: Route objects to draw. Each needs either 'encoded_polyline'
                (the overview_polyline field returned by neshan_direction and its
                variants) or a raw 'coordinates' list.
            show_traffic: Overlay live traffic layer on the map.
            show_poi: Show points of interest labels on the map.
            map_key: Neshan Web SDK API key (different from service key).
                     Without this the base map tiles won't load, but markers
                     and routes are still drawn. Get one from platform.neshan.org.
        """
        return await handlers.handle_map_view(
            center_lat=center_lat,
            center_lng=center_lng,
            zoom=zoom,
            markers=markers,
            routes=routes,
            title=title,
            show_traffic=show_traffic,
            show_poi=show_poi,
            map_key=map_key,
        )
