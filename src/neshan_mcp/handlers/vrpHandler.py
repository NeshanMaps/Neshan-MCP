"""Handler for the VRP logistic domain."""

from __future__ import annotations

from ..schemas.vrp import VRPInput
from ..services import NeshanClient, vrpService
from ..utils import handle_api_errors


@handle_api_errors
async def handle_vrp_logistic(client: NeshanClient, **kwargs) -> dict:
    return await vrpService.vrp_logistic(client, VRPInput(**kwargs))
