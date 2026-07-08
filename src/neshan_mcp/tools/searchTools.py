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
            field list), with each item annotated with a boolean
            'verified_details_available'. Only items where this is true have an
            owner-claimed profile and a 'poiHash' — pass that hash to
            neshan_get_point_by_hash to fetch confirmed details (working hours,
            phone, etc.).

            Items where 'verified_details_available' is false have NO data in
            Neshan at all (not "closed" — simply unverified). Do not exclude
            them from results or assume they don't meet the query's criteria.
            neshan_get_point_by_hash is expensive, so call it selectively (e.g.
            only for the few candidates you actually need confirmed info on),
            not for every result. When answering a question like "which cafes
            are open at 8am", report it as e.g. "3 confirmed open; 12 more have
            no hours data and may also be open."
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
