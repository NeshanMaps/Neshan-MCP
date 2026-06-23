"""Handler for the zipcode domain."""

from __future__ import annotations

from ..schemas.zipcode import ZipcodeInput
from ..services import NeshanClient, zipcodeService
from ..utils import handle_api_errors


@handle_api_errors
async def handle_zipcode(client: NeshanClient, **kwargs) -> dict:
    return await zipcodeService.zipcode_lookup(client, ZipcodeInput(**kwargs))
