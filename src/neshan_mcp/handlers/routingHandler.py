"""Handlers for the routing domain."""

from __future__ import annotations

from typing import Any

from ..schemas.routing import DirectionInput, MapMatchingInput, MatrixInput, TspInput
from ..services import NeshanClient, routingService
from ..utils import handle_api_errors


@handle_api_errors
async def handle_direction(client: NeshanClient, **kwargs) -> dict[str, Any]:
    return await routingService.direction(client, DirectionInput(**kwargs))


@handle_api_errors
async def handle_direction_no_traffic(client: NeshanClient, **kwargs) -> dict[str, Any]:
    return await routingService.direction_no_traffic(client, DirectionInput(**kwargs))


@handle_api_errors
async def handle_distance_matrix(
    client: NeshanClient, origins: list[list[float]], destinations: list[list[float]]
) -> dict[str, Any]:
    return await routingService.distance_matrix(
        client, MatrixInput(origins=origins, destinations=destinations)
    )


@handle_api_errors
async def handle_tsp(client: NeshanClient, **kwargs) -> dict[str, Any]:
    return await routingService.tsp(client, TspInput(**kwargs))


@handle_api_errors
async def handle_map_matching(
    client: NeshanClient, path_points: list[list[float]]
) -> dict[str, Any]:
    return await routingService.map_matching(client, MapMatchingInput(path_points=path_points))
