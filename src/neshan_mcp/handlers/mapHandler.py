"""Handlers for the map domain (static map)."""

from __future__ import annotations

import base64

from ..schemas.map import StaticMapInput
from ..services import NeshanClient, mapService
from ..utils import handle_api_errors

try:
    from fastmcp.utilities.types import Image
except Exception:  # pragma: no cover
    Image = None


@handle_api_errors
async def handle_static_map(client: NeshanClient, **kwargs):
    data = StaticMapInput(**kwargs)
    png = await mapService.static_map(client, data)
    if Image is not None:
        return Image(data=png, format="png")
    return {"mime_type": "image/png", "base64": base64.b64encode(png).decode("ascii")}
