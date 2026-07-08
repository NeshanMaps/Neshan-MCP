"""Handlers for the search domain."""

from __future__ import annotations

from typing import Any

from ..schemas.search import GeocodeInput, GeocodePlusInput, ReverseInput, SearchInput
from ..services import NeshanClient, searchService
from ..utils import handle_api_errors, point_links


def _attach_geocode_links(result: dict) -> None:
    """Add neshan_links to a geocode result that carries top-level lat/lng."""
    ilat = result.get("lat") or result.get("latitude")
    ilng = result.get("lng") or result.get("longitude")
    if ilat is not None and ilng is not None:
        result["neshan_links"] = point_links(ilat, ilng)


def _annotate_verified_details(result: dict) -> dict:
    """Flag whether each item has an owner-claimed profile (poiHash).

    Unclaimed places have no working-hours/phone/etc. data in Neshan at
    all — 'verified_details_available: false' means "unknown", not
    "closed". Calling neshan_get_point_by_hash only works for items
    where this is true, and it's an expensive call, so callers should
    fetch it selectively rather than for every result.
    """
    for item in result.get("items", []):
        if isinstance(item, dict):
            item["verified_details_available"] = "poiHash" in item
    return result


@handle_api_errors
async def handle_search(
    client: NeshanClient,
    term: str,
    lat: float,
    lng: float,
    *,
    sw_lat: float | None = None,
    sw_lng: float | None = None,
    ne_lat: float | None = None,
    ne_lng: float | None = None,
    layer_slug: str | None = None,
) -> dict[str, Any]:
    result = await searchService.search(
        client,
        SearchInput(
            term=term, lat=lat, lng=lng,
            sw_lat=sw_lat, sw_lng=sw_lng, ne_lat=ne_lat, ne_lng=ne_lng,
            layer_slug=layer_slug,
        ),
    )
    return _annotate_verified_details(result)


@handle_api_errors
async def handle_reverse_geocode(client: NeshanClient, lat: float, lng: float) -> dict[str, Any]:
    result = await searchService.reverse_geocode(client, ReverseInput(lat=lat, lng=lng))
    result["neshan_links"] = point_links(lat, lng)
    return result


@handle_api_errors
async def handle_geocode(client: NeshanClient, address: str) -> dict[str, Any]:
    result = await searchService.geocode(client, GeocodeInput(address=address))
    _attach_geocode_links(result)
    return result


@handle_api_errors
async def handle_geocode_plus(client: NeshanClient, **kwargs) -> dict[str, Any]:
    result = await searchService.geocode_plus(client, GeocodePlusInput(**kwargs))
    _attach_geocode_links(result)
    return result
