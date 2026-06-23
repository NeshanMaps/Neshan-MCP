"""MCP tool definitions for the VRP logistic domain."""

from __future__ import annotations

from typing import Any

from .. import handlers
from ..services import NeshanClient


def register(mcp, client: NeshanClient) -> None:
    @mcp.tool
    async def neshan_vrp_logistic(
        vehicles: list[dict[str, Any]],
        jobs: list[dict[str, Any]],
        depot: dict[str, Any],
        plan_time: int = 45000,
        solution_strategy: str = "BEST_EFFORT",
        cost_type: str = "DISTANCE",
        exploration_level: str = "MEDIUM",
        routing_engine: str = "typical",
        balance_workload: bool = False,
        use_time_balancing: bool = False,
        use_traffic_multiplier: bool = False,
    ):
        """Solve a Vehicle Routing Problem (VRP) for logistics / delivery optimization.

        Assigns a set of jobs to vehicles starting from a depot, minimising total
        distance or duration, respecting vehicle capacities, skills, and time windows.

        Args:
            vehicles: List of vehicle objects. Each must include:
                - id (int|str)
                - capacity (int)
                - skills (list[int])
                - timeWindow: {from: "HH:MM:SS", to: "HH:MM:SS"}
                - startLocation / endLocation (optional): {latitude, longitude}

            jobs: List of job objects. Each must include:
                - id (int|str)
                - location: {latitude, longitude}
                - setUpTime (int, seconds)
                - serviceTime (int, seconds)
                - delivery (int), pickup (int), priority (int)
                - skills (list[int])
                - timeWindows: [{from: "HH:MM:SS", to: "HH:MM:SS"}]

            depot: Starting/ending point — {latitude, longitude}.
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
