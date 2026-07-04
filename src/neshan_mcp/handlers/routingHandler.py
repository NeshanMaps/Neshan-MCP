"""Handlers for the routing domain."""

from __future__ import annotations

from typing import Any, Literal

from ..schemas.routing import DirectionInput, HistoricalDirectionInput, IsochroneInput, MapMatchingInput, MatrixInput, TspInput
from ..services import NeshanClient, routingService
from ..utils import handle_api_errors, routing_links

TrafficMode = Literal["live", "no_traffic", "typical", "historical"]

_DIRECTION_SERVICE = {
    "live": routingService.direction,
    "no_traffic": routingService.direction_no_traffic,
    "typical": routingService.direction_typical,
}


def _attach_direction_links(result: dict, data: DirectionInput) -> None:
    result["neshan_links"] = routing_links(
        data.origin_lat, data.origin_lng, data.dest_lat, data.dest_lng, data.vehicle
    )


def _attach_historical_links(result: dict, data: HistoricalDirectionInput) -> None:
    result["neshan_links"] = routing_links(
        data.origin_lat, data.origin_lng, data.dest_lat, data.dest_lng
    )


@handle_api_errors
async def handle_direction(
    client: NeshanClient,
    *,
    origin_lat: float,
    origin_lng: float,
    dest_lat: float,
    dest_lng: float,
    traffic_mode: TrafficMode = "live",
    vehicle: str = "car",
    waypoints: list[list[float]] | None = None,
    avoid_traffic_zone: bool = False,
    avoid_odd_even_zone: bool = False,
    alternative: bool = False,
    bearing: int | None = None,
    routing_type: str | None = None,
    date_time: str | None = None,
) -> dict[str, Any]:
    if traffic_mode == "historical":
        if vehicle != "car" or waypoints or avoid_odd_even_zone or bearing is not None:
            raise ValueError(
                "vehicle (other than 'car'), waypoints, avoid_odd_even_zone, and bearing "
                "are not supported when traffic_mode='historical'"
            )
        if routing_type is None or date_time is None:
            raise ValueError("routing_type and date_time are required when traffic_mode='historical'")
        data = HistoricalDirectionInput(
            origin_lat=origin_lat, origin_lng=origin_lng,
            dest_lat=dest_lat, dest_lng=dest_lng,
            routing_type=routing_type, date_time=date_time,
            avoid_traffic_zone=avoid_traffic_zone, alternative=alternative,
        )
        result = await routingService.direction_historical(client, data)
        _attach_historical_links(result, data)
        return result

    if routing_type is not None or date_time is not None:
        raise ValueError("routing_type and date_time only apply when traffic_mode='historical'")
    if traffic_mode == "no_traffic" and bearing is not None:
        raise ValueError("'bearing' is not supported when traffic_mode='no_traffic'")

    data = DirectionInput(
        origin_lat=origin_lat, origin_lng=origin_lng,
        dest_lat=dest_lat, dest_lng=dest_lng,
        vehicle=vehicle, waypoints=waypoints,
        avoid_traffic_zone=avoid_traffic_zone, avoid_odd_even_zone=avoid_odd_even_zone,
        alternative=alternative, bearing=bearing,
    )
    result = await _DIRECTION_SERVICE[traffic_mode](client, data)
    _attach_direction_links(result, data)
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
