"""MCP tool definitions for the point domain."""

from __future__ import annotations

from .. import handlers
from ..services import NeshanClient


def register(mcp, client: NeshanClient) -> None:
    @mcp.tool
    async def neshan_get_point_by_hash(hash: str):
        """Fetch full details of a place using its poiHash from neshan_search results.

        Call this after neshan_search when you need richer information about a specific
        result — precise address, category, coordinates, neighbourhood, working hours, and region.

        Args:
            hash: The poiHash value taken from a result item returned by neshan_search.

        Returns:
            Raw Neshan point response (see platform.neshan.org docs), plus a
            top-level 'neshan_links' entry for opening it in the Neshan app/web.
        """
        return await handlers.handle_get_point(client, hash)
