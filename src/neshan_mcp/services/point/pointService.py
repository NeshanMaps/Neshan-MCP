"""Raw API wrapper for the point domain."""

from __future__ import annotations

from typing import Any

from ...constants import Endpoints
from ...schemas.point import PointInput
from ..base import NeshanClient


async def get_point(client: NeshanClient, data: PointInput) -> dict[str, Any]:
    return await client.get_json(
        Endpoints.POINT, service="point",
        params={"hash": data.hash},
    )
