"""MCP tool definitions for the point domain."""

from __future__ import annotations

from .. import handlers
from ..services import NeshanClient


def register(mcp, client: NeshanClient) -> None:
    @mcp.tool
    async def neshan_get_point_by_hash(hash: str):
        """Fetch full details of a place using its poiHash from neshan_search results.

        Only works for items where neshan_search marked
        'verified_details_available: true' (owner-claimed places). This call is
        expensive — use it selectively for specific candidates you need confirmed
        details on (precise address, category, working hours, region), not as a
        blanket follow-up for every search result.

        Args:
            hash: The poiHash value taken from a result item returned by neshan_search.

        Returns:
            Raw Neshan point response (see platform.neshan.org docs), plus a
            top-level 'neshan_links' entry for opening it in the Neshan app/web.
        """
        return await handlers.handle_get_point(client, hash)
