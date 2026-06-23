"""Raw API wrapper for the VRP logistic domain."""

from __future__ import annotations

from ...constants import Endpoints
from ...schemas.vrp import VRPInput
from ..base import NeshanClient


async def vrp_logistic(client: NeshanClient, data: VRPInput) -> dict:
    return await client.post_json(
        Endpoints.VRP_LOGISTIC,
        service="vrp",
        body=data.model_dump(by_alias=True, exclude_none=True),
    )
