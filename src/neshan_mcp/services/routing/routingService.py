"""Raw API wrappers for the routing domain."""

from __future__ import annotations

from ...constants import Endpoints
from ...schemas.routing import DirectionInput, IsochroneInput, MapMatchingInput, MatrixInput, TspInput
from ...utils import coord, coord_list
from ..base import NeshanClient
from .types import DirectionResponse, IsochroneResponse, MapMatchingResponse, MatrixResponse, TspResponse


def _direction_params(data: DirectionInput) -> dict:
    params = {
        "type": data.vehicle,
        "origin": coord(data.origin_lat, data.origin_lng),
        "destination": coord(data.dest_lat, data.dest_lng),
        "avoidTrafficZone": str(data.avoid_traffic_zone).lower(),
        "avoidOddEvenZone": str(data.avoid_odd_even_zone).lower(),
        "alternative": str(data.alternative).lower(),
    }
    if data.waypoints:
        params["waypoints"] = coord_list(data.waypoints)
    if data.bearing is not None:
        params["bearing"] = data.bearing
    return params


async def direction(client: NeshanClient, data: DirectionInput) -> DirectionResponse:
    return await client.get_json(
        Endpoints.DIRECTION, service="routing", params=_direction_params(data)
    )


async def direction_no_traffic(
    client: NeshanClient, data: DirectionInput
) -> DirectionResponse:
    params = _direction_params(data)
    params.pop("bearing", None)
    return await client.get_json(
        Endpoints.DIRECTION_NO_TRAFFIC, service="routing", params=params
    )


async def distance_matrix(client: NeshanClient, data: MatrixInput) -> MatrixResponse:
    return await client.get_json(
        Endpoints.DISTANCE_MATRIX, service="matrix",
        params={
            "origins": coord_list(data.origins),
            "destinations": coord_list(data.destinations),
        },
    )


async def tsp(client: NeshanClient, data: TspInput) -> TspResponse:
    return await client.get_json(
        Endpoints.TSP, service="tsp",
        params={
            "waypoints": coord_list(data.waypoints),
            "roundTrip": str(data.round_trip).lower(),
            "sourceIsAnyPoint": str(data.source_is_any_point).lower(),
            "lastIsAnyPoint": str(data.last_is_any_point).lower(),
        },
    )


async def map_matching(client: NeshanClient, data: MapMatchingInput) -> MapMatchingResponse:
    # [VERIFY] endpoint path/param not confirmed against live docs.
    return await client.get_json(
        Endpoints.MAP_MATCHING, service="map_matching",
        params={"path": coord_list(data.path_points)},
    )


async def isochrone(client: NeshanClient, data: IsochroneInput) -> IsochroneResponse:
    params: dict = {
        "location": coord(data.lat, data.lng),
        "polygon": str(data.polygon).lower(),
        "denoise": data.denoise,
    }
    if data.distance is not None:
        params["distance"] = data.distance
    if data.time is not None:
        params["time"] = data.time
    return await client.get_json(Endpoints.ISOCHRONE, service="isochrone", params=params)
