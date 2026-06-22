"""Constant values: base URL, endpoint paths/versions, header + key-env mappings."""

from __future__ import annotations

import os

BASE_URL = os.getenv("NESHAN_BASE_URL", "https://api.neshan.org")


class Endpoints:
    """Relative paths under BASE_URL. Versions kept explicit for easy bumps."""

    SEARCH = "/v1/search"                               # [verified]
    REVERSE = "/v5/reverse"                             # [verified]
    GEOCODING = "/geocoding/v1/"                        # [verified] json={...}
    GEOCODING_PLUS = "/geocoding/v1/plus"               # [verified] json={...}
    DIRECTION = "/v4/direction"                         # [verified]
    DIRECTION_NO_TRAFFIC = "/v4/direction/no-traffic"   # [verified]
    DISTANCE_MATRIX = "/v1/distance-matrix"             # [verified]
    TSP = "/v3/trip"                                    # [verified]
    STATIC_MAP = "/v5/static"                           # [verified] key in query
    # [VERIFY] path/params not confirmed against live docs.
    MAP_MATCHING = os.getenv("NESHAN_MAP_MATCHING_PATH", "/mapMatching/v1/snapToRoad")


# Client header names (lowercased; FastMCP lowercases header keys).
HEADER_BASE = "neshan-api-key"
HEADER_ALIAS = "api-key"

# Per-service env override variables (fall back to NESHAN_API_KEY).
KEY_OVERRIDE_ENV = {
    "search": "NESHAN_KEY_SEARCH",
    "geocoding": "NESHAN_KEY_GEOCODING",
    "routing": "NESHAN_KEY_ROUTING",
    "matrix": "NESHAN_KEY_MATRIX",
    "tsp": "NESHAN_KEY_TSP",
    "static": "NESHAN_KEY_STATIC",
    "map_matching": "NESHAN_KEY_MAP_MATCHING",
}
