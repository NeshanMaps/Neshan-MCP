"""MCP tool definitions for the routing domain."""

from __future__ import annotations

from .. import handlers
from ..services import NeshanClient


def register(mcp, client: NeshanClient) -> None:
    @mcp.tool
    async def neshan_direction(
        origin_lat: float, origin_lng: float, dest_lat: float, dest_lng: float,
        vehicle: str = "car", waypoints: list[list[float]] | None = None,
        avoid_traffic_zone: bool = False, avoid_odd_even_zone: bool = False,
        alternative: bool = False, bearing: int | None = None,
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
        origin_lat: float, origin_lng: float, dest_lat: float, dest_lng: float,
        vehicle: str = "car", waypoints: list[list[float]] | None = None,
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
    async def neshan_isochrone(
        lat: float,
        lng: float,
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
