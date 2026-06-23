"""Raw API wrapper for the zipcode domain."""

from __future__ import annotations

from ...constants import Endpoints
from ...schemas.zipcode import ZipcodeInput
from ..base import NeshanClient


async def zipcode_lookup(client: NeshanClient, data: ZipcodeInput) -> dict:
    return await client.get_json(
        Endpoints.ZIPCODE,
        service="zipcode",
        params={"zipcode": data.zipcode},
    )
