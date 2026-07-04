"""MCP tool definitions for the routing domain."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field

from .. import handlers
from ..schemas.routing.common import Vehicle
from ..schemas.shared import Latitude, Longitude
from ..services import NeshanClient

Bearing = Annotated[int, Field(ge=0, le=360)]


def register(mcp, client: NeshanClient) -> None:
    @mcp.tool
    async def neshan_direction(
        origin_lat: Latitude, origin_lng: Longitude, dest_lat: Latitude, dest_lng: Longitude,
        vehicle: Vehicle = "car", waypoints: list[list[float]] | None = None,
        avoid_traffic_zone: bool = False, avoid_odd_even_zone: bool = False,
        alternative: bool = False, bearing: Bearing | None = None,
    ):
        """Calculate a route between two points using LIVE traffic.

        Args:
            origin_lat, origin_lng: Start point.
            dest_lat, dest_lng: End point.
            vehicle: 'car' or 'motorcycle'.
            waypoints: Optional ordered stops as [[lat, lng], ...].
            avoid_traffic_zone: Avoid the central traffic (طرح ترافیک) zone.
            avoid_odd_even_zone: Avoid the odd/even (زوج و فرد) zone.
            alternative: Also return alternative routes.
            bearing: Optional heading (0-360) at the origin.
        """
        return await handlers.handle_direction(
            client, origin_lat=origin_lat, origin_lng=origin_lng,
            dest_lat=dest_lat, dest_lng=dest_lng, vehicle=vehicle,
            waypoints=waypoints, avoid_traffic_zone=avoid_traffic_zone,
            avoid_odd_even_zone=avoid_odd_even_zone, alternative=alternative, bearing=bearing,
        )

    @mcp.tool
    async def neshan_direction_no_traffic(
        origin_lat: Latitude, origin_lng: Longitude, dest_lat: Latitude, dest_lng: Longitude,
        vehicle: Vehicle = "car", waypoints: list[list[float]] | None = None,
        avoid_traffic_zone: bool = False, avoid_odd_even_zone: bool = False,
        alternative: bool = False,
    ):
        """Calculate a route based on STATIC (no live) traffic."""
        return await handlers.handle_direction_no_traffic(
            client, origin_lat=origin_lat, origin_lng=origin_lng,
            dest_lat=dest_lat, dest_lng=dest_lng, vehicle=vehicle,
            waypoints=waypoints, avoid_traffic_zone=avoid_traffic_zone,
            avoid_odd_even_zone=avoid_odd_even_zone, alternative=alternative,
        )

    @mcp.tool
    async def neshan_distance_matrix(
        origins: list[list[float]], destinations: list[list[float]]
    ):
        """Compute travel distance and duration for every origin-destination pair.

        Args:
            origins: Origin points as [[lat, lng], ...].
            destinations: Destination points as [[lat, lng], ...].
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
        """
        return await handlers.handle_tsp(
            client, waypoints=waypoints, round_trip=round_trip,
            source_is_any_point=source_is_any_point, last_is_any_point=last_is_any_point,
        )

    @mcp.tool
    async def neshan_map_matching(path_points: list[list[float]]):
        """Snap a sequence of GPS points onto the road network (map matching).

        NOTE: endpoint/params are unverified in this build.

        Args:
            path_points: The recorded track as [[lat, lng], ...].
        """
        return await handlers.handle_map_matching(client, path_points)

    @mcp.tool
    async def neshan_direction_pedestrian(
        origin_lat: Latitude, origin_lng: Longitude,
        dest_lat: Latitude, dest_lng: Longitude,
        waypoints: list[list[float]] | None = None,
        alternative: bool = False,
        bearing: Bearing | None = None,
    ):
        """Calculate the best walking route between two points (pedestrian routing).

        Uses safe, pedestrian-friendly paths. Returns the same route structure as
        neshan_direction but optimised for on-foot travel.

        Args:
            origin_lat, origin_lng: Start point.
            dest_lat, dest_lng: End point.
            waypoints: Optional intermediate stops as [[lat, lng], ...].
            alternative: Return alternative routes if available.
            bearing: Optional heading (0-360) at the origin.
        """
        return await handlers.handle_direction(
            client,
            origin_lat=origin_lat, origin_lng=origin_lng,
            dest_lat=dest_lat, dest_lng=dest_lng,
            vehicle="pedestrian",
            waypoints=waypoints,
            avoid_traffic_zone=False,
            avoid_odd_even_zone=False,
            alternative=alternative,
            bearing=bearing,
        )

    @mcp.tool
    async def neshan_direction_typical(
        origin_lat: Latitude, origin_lng: Longitude,
        dest_lat: Latitude, dest_lng: Longitude,
        waypoints: list[list[float]] | None = None,
        avoid_traffic_zone: bool = False,
        avoid_odd_even_zone: bool = False,
        alternative: bool = False,
        bearing: Bearing | None = None,
    ):
        """Calculate a car route using typical (pattern-based) traffic updated every 15 minutes.

        Useful for reliable ETA estimates when live traffic is unavailable or unstable.

        Args:
            origin_lat, origin_lng: Start point.
            dest_lat, dest_lng: End point.
            waypoints: Optional intermediate stops as [[lat, lng], ...].
            avoid_traffic_zone: Avoid the central traffic (طرح ترافیک) zone.
            avoid_odd_even_zone: Avoid the odd/even (زوج و فرد) zone.
            alternative: Return alternative routes if available.
            bearing: Optional heading (0-360) at the origin.
        """
        return await handlers.handle_direction_typical(
            client,
            origin_lat=origin_lat, origin_lng=origin_lng,
            dest_lat=dest_lat, dest_lng=dest_lng,
            vehicle="car",
            waypoints=waypoints,
            avoid_traffic_zone=avoid_traffic_zone,
            avoid_odd_even_zone=avoid_odd_even_zone,
            alternative=alternative,
            bearing=bearing,
        )

    @mcp.tool
    async def neshan_direction_historical(
        origin_lat: Latitude, origin_lng: Longitude,
        dest_lat: Latitude, dest_lng: Longitude,
        routing_type: Literal["DepartAt", "ArriveAt"],
        date_time: str,
        avoid_traffic_zone: bool = False,
        alternative: bool = False,
    ):
        """Calculate the best car route for a future date/time using historical traffic data.

        Currently available for Tehran, Mashhad, and Karaj only.
        Supports planning up to one week ahead.

        Args:
            origin_lat, origin_lng: Start point.
            dest_lat, dest_lng: End point.
            routing_type: 'DepartAt' to specify departure time, 'ArriveAt' for arrival time.
            date_time: Target date and time in 'YYYY-MM-DDThh:mm' format (no timezone, UTC+0).
            avoid_traffic_zone: Avoid the central traffic (طرح ترافیک) zone.
            alternative: Return alternative routes if available.
        """
        return await handlers.handle_direction_historical(
            client,
            origin_lat=origin_lat, origin_lng=origin_lng,
            dest_lat=dest_lat, dest_lng=dest_lng,
            routing_type=routing_type,
            date_time=date_time,
            avoid_traffic_zone=avoid_traffic_zone,
            alternative=alternative,
        )

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
