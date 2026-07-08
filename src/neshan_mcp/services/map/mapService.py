"""Raw API wrapper for the map domain.

The static map service takes the key as a `key=` query parameter (not the
Api-Key header) and returns PNG bytes, not JSON.
"""

from __future__ import annotations

from ...constants import Endpoints
from ...schemas.map import StaticMapArcInput, StaticMapInput
from ..base import NeshanClient
from .types import StaticMapResponse


async def static_map(client: NeshanClient, data: StaticMapInput) -> StaticMapResponse:
    return await client.get_bytes_with_query_key(
        Endpoints.STATIC_MAP, service="static",
        params={
            "type": data.map_type,
            "zoom": data.zoom,
            "width": data.width,
            "height": data.height,
            "latitude": data.lat,
            "longitude": data.lng,
            "marker": data.marker,
        },
    )


async def static_map_arc(client: NeshanClient, data: StaticMapArcInput) -> StaticMapResponse:
    params: dict = {
        "type": data.map_type,
        "from": f"{data.origin_lat},{data.origin_lng}",
        "to": f"{data.dest_lat},{data.dest_lng}",
        "width": data.width,
        "height": data.height,
        "dashed": str(data.dashed).lower(),
    }
    if data.color is not None:
        params["color"] = data.color
    if data.marker1_token is not None:
        params["marker1Token"] = data.marker1_token
    if data.marker2_token is not None:
        params["marker2Token"] = data.marker2_token
    return await client.get_bytes_with_query_key(
        Endpoints.STATIC_MAP_ARC, service="static_arc", params=params,
    )
