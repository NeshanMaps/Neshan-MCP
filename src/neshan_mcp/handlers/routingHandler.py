"""Handlers for the routing domain."""

from __future__ import annotations

from typing import Any

from ..schemas.routing import DirectionInput, HistoricalDirectionInput, IsochroneInput, MapMatchingInput, MatrixInput, TspInput
from ..services import NeshanClient, routingService
from ..utils import handle_api_errors, routing_links


def _attach_direction_links(result: dict, data: DirectionInput) -> None:
    result["neshan_links"] = routing_links(
        data.origin_lat, data.origin_lng, data.dest_lat, data.dest_lng, data.vehicle
    )


def _attach_historical_links(result: dict, data: HistoricalDirectionInput) -> None:
    result["neshan_links"] = routing_links(
        data.origin_lat, data.origin_lng, data.dest_lat, data.dest_lng
    )


@handle_api_errors
async def handle_direction(client: NeshanClient, **kwargs) -> dict[str, Any]:
    data = DirectionInput(**kwargs)
    result = await routingService.direction(client, data)
    _attach_direction_links(result, data)
    return result


@handle_api_errors
async def handle_direction_no_traffic(client: NeshanClient, **kwargs) -> dict[str, Any]:
    data = DirectionInput(**kwargs)
    result = await routingService.direction_no_traffic(client, data)
    _attach_direction_links(result, data)
    return result


@handle_api_errors
async def handle_direction_typical(client: NeshanClient, **kwargs) -> dict[str, Any]:
    data = DirectionInput(**kwargs)
    result = await routingService.direction_typical(client, data)
    _attach_direction_links(result, data)
    return result


@handle_api_errors
async def handle_direction_historical(client: NeshanClient, **kwargs) -> dict[str, Any]:
    data = HistoricalDirectionInput(**kwargs)
    result = await routingService.direction_historical(client, data)
    _attach_historical_links(result, data)
    return result


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


@handle_api_errors
async def handle_isochrone(client: NeshanClient, **kwargs) -> dict[str, Any]:
    return await routingService.isochrone(client, IsochroneInput(**kwargs))
