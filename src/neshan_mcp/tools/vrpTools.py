"""MCP tool definitions for the VRP logistic domain."""

from __future__ import annotations

from typing import Literal

from .. import handlers
from ..schemas.vrp import VRPJob, VRPLocation, VRPVehicle
from ..services import NeshanClient


def register(mcp, client: NeshanClient) -> None:
    @mcp.tool
    async def neshan_vrp_logistic(
        vehicles: list[VRPVehicle],
        jobs: list[VRPJob],
        depot: VRPLocation,
        plan_time: int = 45000,
        solution_strategy: Literal["BEST_EFFORT", "FAST", "THOROUGH"] = "BEST_EFFORT",
        cost_type: Literal["DISTANCE", "DURATION"] = "DISTANCE",
        exploration_level: Literal["LOW", "MEDIUM", "HIGH"] = "MEDIUM",
        routing_engine: Literal["typical", "car", "motorcycle"] = "typical",
        balance_workload: bool = False,
        use_time_balancing: bool = False,
        use_traffic_multiplier: bool = False,
    ):
        """Solve a Vehicle Routing Problem (VRP) for logistics / delivery optimization.

        Assigns a set of jobs to vehicles starting from a depot, minimising total
        distance or duration, respecting vehicle capacities, skills, and time windows.
        See each object's field descriptions in the tool schema for exact shape.

        Args:
            vehicles: Vehicles available to plan routes for.
            jobs: Jobs to assign to vehicles. 'skills' on a job must be a subset of
                the assigned vehicle's 'skills' to be eligible.
            depot: Starting/ending point shared by vehicles without their own
                startLocation/endLocation.
            plan_time: Max solver time in milliseconds (default 45000).
            solution_strategy: 'BEST_EFFORT' | 'FAST' | 'THOROUGH'.
            cost_type: Optimise for 'DISTANCE' or 'DURATION'.
            exploration_level: 'LOW' | 'MEDIUM' | 'HIGH'.
            routing_engine: 'typical' | 'car' | 'motorcycle'.
            balance_workload: Distribute jobs evenly across vehicles.
            use_time_balancing: Balance travel time across vehicles.
            use_traffic_multiplier: Apply live traffic to duration estimates.

        Returns:
            - routes: Per-vehicle route with distance, duration, encoded geometry, and ordered steps.
            - summary: Total distance, duration, routes count, unassigned jobs count.
            - violationMessages: Any constraint violations.
        """
        return await handlers.handle_vrp_logistic(
            client,
            vehicles=vehicles,
            jobs=jobs,
            depot=depot,
            planTime=plan_time,
            solutionStrategy=solution_strategy,
            costType=cost_type,
            explorationLevel=exploration_level,
            routingEngine=routing_engine,
            balanceWorkload=balance_workload,
            useTimeBalancing=use_time_balancing,
            useTrafficMultiplier=use_traffic_multiplier,
        )
