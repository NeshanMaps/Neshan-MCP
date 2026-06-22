"""Resolve the API key: client HTTP header first, env fallback (stdio).

HTTP mode (primary): the client sends the key per request:
    Neshan-Api-Key: <key>
    Neshan-Api-Key-<service>: <key>   # optional per-service override
    Api-Key: <key>                    # accepted alias
"""

from __future__ import annotations

from fastmcp.server.dependencies import get_http_headers

from ..appConfig import env_key_for
from ..constants import HEADER_ALIAS, HEADER_BASE


def resolve_key(service: str) -> str:
    headers = get_http_headers()  # {} outside an HTTP request (stdio)
    if headers:
        svc = f"{HEADER_BASE}-{service}"
        if headers.get(svc):
            return headers[svc]
        if headers.get(HEADER_BASE):
            return headers[HEADER_BASE]
        if headers.get(HEADER_ALIAS):
            return headers[HEADER_ALIAS]
    return env_key_for(service)
