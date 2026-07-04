"""Raw API wrappers for the search domain."""

from __future__ import annotations

import json

from ...constants import Endpoints
from ...schemas.search import GeocodeInput, GeocodePlusInput, ReverseInput, SearchInput
from ..base import NeshanClient
from .types import GeocodeResponse, ReverseResponse, SearchResponse


async def search(client: NeshanClient, data: SearchInput) -> SearchResponse:
    return await client.get_json(
        Endpoints.SEARCH, service="search",
        params={"q": json.dumps(data.to_payload(), ensure_ascii=False)},
    )


async def reverse_geocode(client: NeshanClient, data: ReverseInput) -> ReverseResponse:
    return await client.get_json(
        Endpoints.REVERSE, service="search",
        params={"lat": data.lat, "lng": data.lng},
    )


async def geocode(client: NeshanClient, data: GeocodeInput) -> GeocodeResponse:
    payload = {"address": data.address}
    return await client.get_json(
        Endpoints.GEOCODING, service="geocoding",
        params={"json": json.dumps(payload, ensure_ascii=False)},
    )


async def geocode_plus(client: NeshanClient, data: GeocodePlusInput) -> GeocodeResponse:
    return await client.get_json(
        Endpoints.GEOCODING_PLUS, service="geocoding",
        params={"json": json.dumps(data.to_payload(), ensure_ascii=False)},
    )
