"""Request handlers grouped by domain."""

from .mapHandler import handle_static_map
from .routingHandler import (
    handle_direction,
    handle_direction_historical,
    handle_direction_no_traffic,
    handle_direction_typical,
    handle_distance_matrix,
    handle_isochrone,
    handle_map_matching,
    handle_tsp,
)
from .searchHandler import (
    handle_geocode,
    handle_geocode_plus,
    handle_reverse_geocode,
    handle_search,
)

__all__ = [
    "handle_search",
    "handle_reverse_geocode",
    "handle_geocode",
    "handle_geocode_plus",
    "handle_direction",
    "handle_direction_no_traffic",
    "handle_direction_typical",
    "handle_direction_historical",
    "handle_distance_matrix",
    "handle_tsp",
    "handle_map_matching",
    "handle_isochrone",
    "handle_static_map",
]
