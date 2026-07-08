"""Raw API wrapper for the traffic analytics domain."""

from __future__ import annotations

from ...constants import Endpoints
from ...schemas.traffic import TrafficAnalyticsInput
from ..base import NeshanClient


async def traffic_analytics(client: NeshanClient, data: TrafficAnalyticsInput) -> dict:
    return await client.get_json(
        Endpoints.TRAFFIC_ANALYTICS,
        service="traffic",
        params={"latitude": data.lat, "longitude": data.lng},
    )


async def traffic_analytics_map(client: NeshanClient, url: str) -> bytes:
    """Fetch the static traffic map PNG from the signed URL returned by traffic_analytics.

    The URL is always under the same base URL; strip the scheme+host to get the path.
    """
    from urllib.parse import urlparse
    path = urlparse(url).path
    return await client.get_bytes(path, service="traffic")
