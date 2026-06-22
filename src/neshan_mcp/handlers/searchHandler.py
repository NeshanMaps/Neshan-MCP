"""Handlers for the search domain."""

from __future__ import annotations

from typing import Any

from ..schemas.search import GeocodeInput, GeocodePlusInput, ReverseInput, SearchInput
from ..services import NeshanClient, searchService
from ..utils import handle_api_errors


@handle_api_errors
async def handle_search(client: NeshanClient, term: str, lat: float, lng: float) -> dict[str, Any]:
    return await searchService.search(client, SearchInput(term=term, lat=lat, lng=lng))


@handle_api_errors
async def handle_reverse_geocode(client: NeshanClient, lat: float, lng: float) -> dict[str, Any]:
    return await searchService.reverse_geocode(client, ReverseInput(lat=lat, lng=lng))


@handle_api_errors
async def handle_geocode(client: NeshanClient, address: str) -> dict[str, Any]:
    return await searchService.geocode(client, GeocodeInput(address=address))


@handle_api_errors
async def handle_geocode_plus(client: NeshanClient, **kwargs) -> dict[str, Any]:
    return await searchService.geocode_plus(client, GeocodePlusInput(**kwargs))
