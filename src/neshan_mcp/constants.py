"""Constant values: base URL, endpoint paths/versions, header + key-env mappings."""

from __future__ import annotations

import os

BASE_URL = os.getenv("NESHAN_BASE_URL", "https://api.neshan.org")


class Endpoints:
    """Relative paths under BASE_URL. Versions kept explicit for easy bumps."""

    SEARCH = "/v3/search"
    REVERSE = "/v5/reverse"
    GEOCODING = "/geocoding/v1"
    GEOCODING_PLUS = "/geocoding/v1/plus"
    DIRECTION = "/v4/direction"
    DIRECTION_NO_TRAFFIC = "/v4/direction/no-traffic"
    DIRECTION_TYPICAL = "/v1/direction/typical"
    DIRECTION_HISTORICAL = "/v1/direction/historical"
    DISTANCE_MATRIX = "/v1/distance-matrix"
    TSP = "/v3/trip"
    STATIC_MAP = "/v5/static"
    STATIC_MAP_ARC = "/v4/static/arc"
    ISOCHRONE = "/v1/isochrone"
    TRAFFIC_ANALYTICS = "/navigation/traffic/analytics/v0.1"
    VRP_LOGISTIC = "/vrp/logistic"
    POINT = "/v1/point"
    MAP_MATCHING = os.getenv("NESHAN_MAP_MATCHING_PATH", "/v3/map-matching")

# Client header names (lowercased; FastMCP lowercases header keys).


HEADER_BASE = "neshan-api-key"
HEADER_ALIAS = "api-key"

# Per-service env override variables (fall back to NESHAN_API_KEY).
KEY_OVERRIDE_ENV = {
    "search": "NESHAN_KEY_SEARCH",
    "geocoding": "NESHAN_KEY_GEOCODING",
    "routing": "NESHAN_KEY_ROUTING",
    "historical": "NESHAN_KEY_HISTORICAL",
    "matrix": "NESHAN_KEY_MATRIX",
    "tsp": "NESHAN_KEY_TSP",
    "static": "NESHAN_KEY_STATIC",
    "static_arc": "NESHAN_KEY_STATIC_ARC",
    "isochrone": "NESHAN_KEY_ISOCHRONE",
    "map_matching": "NESHAN_KEY_MAP_MATCHING",
    "traffic": "NESHAN_KEY_TRAFFIC",
    "vrp": "NESHAN_KEY_VRP",
    "point": "NESHAN_KEY_POINT",
}
