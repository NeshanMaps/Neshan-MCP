"""Handler for the traffic analytics domain."""

from __future__ import annotations

import base64

from ..schemas.traffic import TrafficAnalyticsInput
from ..services import NeshanClient, trafficService
from ..utils import handle_api_errors

try:
    from fastmcp.utilities.types import Image
except Exception:  # pragma: no cover
    Image = None


@handle_api_errors
async def handle_traffic_analytics(client: NeshanClient, **kwargs):
    data = TrafficAnalyticsInput(**kwargs)
    result = await trafficService.traffic_analytics(client, data)

    map_url = result.get("staticMapUrl")
    if map_url:
        png = await trafficService.traffic_analytics_map(client, map_url)
        if Image is not None:
            result["static_map"] = Image(data=png, format="png")
        else:
            result["static_map"] = {
                "mime_type": "image/png",
                "base64": base64.b64encode(png).decode("ascii"),
            }

    return result
