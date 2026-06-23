"""Handlers for the search domain."""

from __future__ import annotations

from typing import Any

from ..schemas.search import GeocodeInput, GeocodePlusInput, ReverseInput, SearchInput
from ..services import NeshanClient, searchService
from ..utils import handle_api_errors, point_links, routing_links


def _attach_point_links(result: dict) -> None:
    """Add neshan_links to each item that carries a location."""
    for item in result.get("items") or []:
        loc = item.get("location") or {}
        ilat, ilng = loc.get("y"), loc.get("x")
        if ilat is not None and ilng is not None:
            item["neshan_links"] = point_links(ilat, ilng)


def _attach_geocode_links(result: dict) -> None:
    """Add neshan_links to a geocode result that carries top-level lat/lng."""
    ilat = result.get("lat") or result.get("latitude")
    ilng = result.get("lng") or result.get("longitude")
    if ilat is not None and ilng is not None:
        result["neshan_links"] = point_links(ilat, ilng)


@handle_api_errors
async def handle_search(client: NeshanClient, term: str, lat: float, lng: float) -> dict[str, Any]:
    result = await searchService.search(client, SearchInput(term=term, lat=lat, lng=lng))
    _attach_point_links(result)
    return result


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
