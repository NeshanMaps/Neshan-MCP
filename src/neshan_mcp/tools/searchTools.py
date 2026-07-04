"""MCP tool definitions for the search domain."""

from __future__ import annotations

from .. import handlers
from ..schemas.shared import Latitude, Longitude
from ..services import NeshanClient


def register(mcp, client: NeshanClient) -> None:
    @mcp.tool
    async def neshan_search(
        term: str,
        lat: Latitude,
        lng: Longitude,
        sw_lat: Latitude | None = None,
        sw_lng: Longitude | None = None,
        ne_lat: Latitude | None = None,
        ne_lng: Longitude | None = None,
        layer_slug: str | None = None,
    ):
        """Search for places, addresses and POIs near a location in Iran.

        Args:
            term: Free-text query in Persian or English (e.g. "کافه").
            lat: Latitude of the search center.
            lng: Longitude of the search center.
            sw_lat / sw_lng: South-west corner of a bounding box to restrict results.
            ne_lat / ne_lng: North-east corner of a bounding box to restrict results.
            layer_slug: Filter results by category/layer slug (e.g. "park").
        """
        return await handlers.handle_search(
            client, term, lat, lng,
            sw_lat=sw_lat, sw_lng=sw_lng, ne_lat=ne_lat, ne_lng=ne_lng,
            layer_slug=layer_slug,
        )

    @mcp.tool
    async def neshan_reverse_geocode(lat: Latitude, lng: Longitude):
        """Convert coordinates into a human-readable Persian address.

        Args:
            lat: Latitude.
            lng: Longitude.
        """
        return await handlers.handle_reverse_geocode(client, lat, lng)

    @mcp.tool
    async def neshan_geocode(address: str):
        """Convert a free-text Persian address into geographic coordinates.

        Args:
            address: The address text (street, plaque, landmark, etc.).
        """
        return await handlers.handle_geocode(client, address)

    @mcp.tool
    async def neshan_geocode_plus(
        address: str,
        city: str | None = None,
        province: str | None = None,
        bias_lat: Latitude | None = None,
        bias_lng: Longitude | None = None,
        sw_lat: Latitude | None = None,
        sw_lng: Longitude | None = None,
        ne_lat: Latitude | None = None,
        ne_lng: Longitude | None = None,
    ):
        """Geocode an address with extra hints for higher accuracy.

        Args:
            address: The address text.
            city: City name to disambiguate.
            province: Province name to disambiguate.
            bias_lat / bias_lng: A location to bias results toward.
            sw_lat / sw_lng: South-west corner of a bounding box.
            ne_lat / ne_lng: North-east corner of a bounding box.
        """
        return await handlers.handle_geocode_plus(
            client, address=address, city=city, province=province,
            bias_lat=bias_lat, bias_lng=bias_lng,
            sw_lat=sw_lat, sw_lng=sw_lng, ne_lat=ne_lat, ne_lng=ne_lng,
        )
