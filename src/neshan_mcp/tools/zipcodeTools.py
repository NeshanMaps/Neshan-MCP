"""MCP tool definitions for the zipcode domain."""

from __future__ import annotations

from .. import handlers
from ..services import NeshanClient


def register(mcp, client: NeshanClient) -> None:
    @mcp.tool
    async def neshan_zipcode(zipcode: str):
        """Look up an Iranian postal code (کد پستی) and return its location and address.

        Returns province, township, zone, village (if rural), full address string, and
        the geographic coordinates (latitude/longitude) of the postal code area.

        Args:
            zipcode: 10-digit Iranian postal code, e.g. '8138718913'.
        """
        return await handlers.handle_zipcode(client, zipcode=zipcode)
