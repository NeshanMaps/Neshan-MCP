"""MCP server factory (mirrors createServer): builds FastMCP, wires client, registers tools."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastmcp import FastMCP

from .services import NeshanClient
from .tools import register_all

INSTRUCTIONS = (
    "Tools for Iran's Neshan Maps Platform: place search, geocoding, reverse "
    "geocoding, routing (car/motorcycle, with/without live traffic), distance "
    "matrix, multi-stop optimization (TSP), and static map images. "
    "Coordinates are (lat, lng) in decimal degrees."
)


def create_server() -> FastMCP:
    client = NeshanClient()

    @asynccontextmanager
    async def lifespan(_server: FastMCP):
        try:
            yield
        finally:
            await client.aclose()

    mcp = FastMCP(name="neshan-mcp", instructions=INSTRUCTIONS, lifespan=lifespan)
    register_all(mcp, client)
    return mcp
