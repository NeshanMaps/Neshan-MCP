"""MCP tool definitions for the routing domain."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field

from .. import handlers
from ..schemas.routing.common import Vehicle
from ..schemas.shared import Latitude, Longitude
from ..services import NeshanClient

Bearing = Annotated[int, Field(ge=0, le=360)]
TrafficMode = Literal["live", "no_traffic", "typical", "historical"]


def register(mcp, client: NeshanClient) -> None:
    @mcp.tool
    async def neshan_direction(
        origin_lat: Latitude, origin_lng: Longitude, dest_lat: Latitude, dest_lng: Longitude,
        traffic_mode: TrafficMode = "live",
        vehicle: Vehicle = "car",
        waypoints: list[list[float]] | None = None,
        avoid_traffic_zone: bool = False,
        avoid_odd_even_zone: bool = False,
        alternative: bool = False,
        bearing: Bearing | None = None,
        routing_type: Literal["DepartAt", "ArriveAt"] | None = None,
        date_time: str | None = None,
    ):
        """Calculate a route between two points, choosing how traffic is modeled.

        Args:
            origin_lat, origin_lng: Start point.
            dest_lat, dest_lng: End point.
            traffic_mode: How to account for traffic when routing:
                - 'live' (default): current real-time traffic. Use for "how long
                  would this take if I left right now".
                - 'no_traffic': static road speeds; traffic is ignored entirely.
                - 'typical': pattern-based traffic refreshed every 15 minutes. Use
                  for a stable ETA when live traffic is flaky or unavailable.
                - 'historical': traffic-aware ETA for a *future* date/time, based
                  on historical patterns for that time of day. Requires
                  routing_type and date_time. Covers Tehran, Mashhad, and Karaj
                  only, up to one week ahead.
            vehicle: 'car', 'motorcycle', or 'pedestrian'. Must stay 'car' (the
                default) when traffic_mode='historical' — that mode has no
                vehicle choice.
            waypoints: Optional ordered stops as [[lat, lng], ...]. Not usable
                with traffic_mode='historical'.
            avoid_traffic_zone: Avoid the central traffic (طرح ترافیک) zone.
            avoid_odd_even_zone: Avoid the odd/even (زوج و فرد) zone. Not usable
                with traffic_mode='historical'.
            alternative: Also return alternative routes.
            bearing: Optional heading (0-360) at the origin. Only usable with
                traffic_mode 'live' or 'typical'.
            routing_type: Required when traffic_mode='historical'. 'DepartAt' to
                specify departure time, 'ArriveAt' for arrival time.
            date_time: Required when traffic_mode='historical'. Target date and
                time as 'YYYY-MM-DDThh:mm' (no timezone, UTC+0).

        Returns:
            Raw Neshan direction response (see platform.neshan.org docs for the
            full field list), including an 'overview_polyline' field that can be
            passed as 'encoded_polyline' to neshan_map_view to draw the route.
            Also includes a top-level 'neshan_links' entry for opening the route
            in the Neshan app/web.
        """
        return await handlers.handle_direction(
            client,
            origin_lat=origin_lat, origin_lng=origin_lng,
            dest_lat=dest_lat, dest_lng=dest_lng,
            traffic_mode=traffic_mode, vehicle=vehicle,
            waypoints=waypoints,
            avoid_traffic_zone=avoid_traffic_zone,
            avoid_odd_even_zone=avoid_odd_even_zone,
            alternative=alternative, bearing=bearing,
            routing_type=routing_type, date_time=date_time,
        )

    @mcp.tool
    async def neshan_distance_matrix(
        origins: list[list[float]], destinations: list[list[float]]
    ):
        """Compute travel distance and duration for every origin-destination pair.

        Args:
            origins: Origin points as [[lat, lng], ...].
            destinations: Destination points as [[lat, lng], ...].

        Returns:
            Raw Neshan distance-matrix response: distance and duration for each
            origin-destination pair (see platform.neshan.org docs for exact shape
            and units).
        """
        return await handlers.handle_distance_matrix(client, origins, destinations)

    @mcp.tool
    async def neshan_tsp(
        waypoints: list[list[float]], round_trip: bool = True,
        source_is_any_point: bool = False, last_is_any_point: bool = False,
    ):
        """Find the optimal visiting order for multiple destinations (TSP).

        Args:
            waypoints: Stops as [[lat, lng], ...] (first item is the start).
            round_trip: If True, the route returns to the start point.
            source_is_any_point: Let the optimizer choose any stop as start.
            last_is_any_point: Let the optimizer choose any stop as the end.

        Returns:
            Raw Neshan trip-optimization response: the optimized visiting order
            and route geometry (see platform.neshan.org docs for exact shape).
        """
        return await handlers.handle_tsp(
            client, waypoints=waypoints, round_trip=round_trip,
            source_is_any_point=source_is_any_point, last_is_any_point=last_is_any_point,
        )

    @mcp.tool
    async def neshan_map_matching(path_points: list[list[float]]):
        """Snap a sequence of GPS points onto the road network (map matching).

        Args:
            path_points: The recorded track as [[lat, lng], ...].

        Returns:
            Raw Neshan map-matching response.
        """
        return await handlers.handle_map_matching(client, path_points)

    @mcp.tool
    async def neshan_isochrone(
        lat: Latitude,
        lng: Longitude,
        distance: float | None = None,
        time: float | None = None,
        polygon: bool = False,
        denoise: float = 0.0,
    ):
        """Calculate the reachable area from a point within a given time or distance (isochrone).

        Returns a GeoJSON FeatureCollection. Each feature's geometry is a Polygon or
        LineString (controlled by 'polygon') and properties.metric is 'time' or 'distance'.
        Both distance and time can be requested simultaneously.

        Args:
            lat: Center latitude.
            lng: Center longitude.
            distance: Max reachable distance in km. At least one of distance/time is required.
            time: Max reachable time in minutes. At least one of distance/time is required.
            polygon: True → Polygon geometry; False → LineString geometry (default False).
            denoise: Simplification level 0–1 (0 = full detail, 1 = maximum simplification).
        """
        return await handlers.handle_isochrone(
            client,
            lat=lat, lng=lng,
            distance=distance, time=time,
            polygon=polygon, denoise=denoise,
        )
