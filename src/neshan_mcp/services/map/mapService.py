"""Raw API wrapper for the map domain.

The static map service takes the key as a `key=` query parameter (not the
Api-Key header) and returns PNG bytes, not JSON.
"""

from __future__ import annotations

from ...constants import Endpoints
from ...schemas.map import StaticMapInput
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
