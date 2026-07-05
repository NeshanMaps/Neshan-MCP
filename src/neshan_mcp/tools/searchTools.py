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

        Returns:
            Raw Neshan search response (see platform.neshan.org docs for the full
            field list). Each item includes a 'neshan_links' entry for opening it
            in the Neshan app/web, and its 'poiHash' can be passed to
            neshan_get_point_by_hash for full place details.
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

        Returns:
            Raw Neshan reverse-geocode response, plus a top-level 'neshan_links' entry.
        """
        return await handlers.handle_reverse_geocode(client, lat, lng)

    @mcp.tool
    async def neshan_geocode(address: str):
        """Convert a free-text Persian address into geographic coordinates.

        Cheaper than neshan_geocode_plus — prefer this by default. Switch to
        neshan_geocode_plus only when the address includes a plaque (پلاک)
        number or refers to a point of interest by name, which this endpoint
        does not resolve.

        Args:
            address: The address text (street, landmark, etc.).

        Returns:
            Raw Neshan geocode response, plus a top-level 'neshan_links' entry.
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
        """Geocode an address that includes a plaque (پلاک) number or a named
        point of interest — neshan_geocode can't resolve those.

        More expensive than neshan_geocode, so only use this when plaque/POI
        resolution is actually needed. Whenever available, pass city,
        province, a bias location, and/or a bounding box: all of them improve
        geocoding accuracy regardless of whether plaque/POI resolution is
        involved.

        Args:
            address: The address text.
            city: City name — improves accuracy.
            province: Province name — improves accuracy.
            bias_lat / bias_lng: A location to bias results toward — improves accuracy.
            sw_lat / sw_lng: South-west corner of a bounding box to restrict results.
            ne_lat / ne_lng: North-east corner of a bounding box to restrict results.

        Returns:
            Raw Neshan geocode response, plus a top-level 'neshan_links' entry.
        """
        return await handlers.handle_geocode_plus(
            client, address=address, city=city, province=province,
            bias_lat=bias_lat, bias_lng=bias_lng,
            sw_lat=sw_lat, sw_lng=sw_lng, ne_lat=ne_lat, ne_lng=ne_lng,
        )
