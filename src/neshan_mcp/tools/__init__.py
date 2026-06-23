"""MCP tool definitions (thin layer delegating to handlers)."""

from __future__ import annotations

from ..services import NeshanClient
from . import mapTools, routingTools, searchTools, trafficTools, utilityTools


def register_all(mcp, client: NeshanClient) -> None:
    searchTools.register(mcp, client)
    routingTools.register(mcp, client)
    mapTools.register(mcp, client)
    trafficTools.register(mcp, client)
    utilityTools.register(mcp, client)
