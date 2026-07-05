"""MCP server factory (mirrors createServer): builds FastMCP, wires client, registers tools."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastmcp import FastMCP

from .services import NeshanClient
from .tools import register_all

INSTRUCTIONS = (
    "Tools for Iran's Neshan Maps Platform: place search, geocoding, reverse "
    "geocoding, routing (car/motorcycle/pedestrian; choose a traffic_mode of "
    "live/no_traffic/typical/historical), isochrone, distance matrix, "
    "multi-stop optimization (TSP), static map images, "
    "Neshan app deeplink generation, and traffic analytics. "
    "Search and routing results include neshan_links (android_web + ios) automatically. "
    "Traffic analytics returns a 24-hour congestion chart, an overall KPI score, "
    "and a static PNG map of the area. "
    "Zipcode lookup resolves an Iranian 10-digit postal code to province, township, "
    "zone, address, and coordinates. "
    "VRP logistic solves fleet routing problems: assigns jobs to vehicles respecting "
    "capacity, skills, and time-windows, and returns optimized routes with geometry. "
    "Point lookup fetches full details of a place (address, category, coordinates, "
    "neighbourhood) using the poiHash returned by neshan_search results. "
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
