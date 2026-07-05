"""Response shaping applied to every handler result.

Hook for trimming verbose API responses before they reach the model. Recurses
through dicts and lists stripping null fields at every level — a missing key
conveys the same "absent" meaning as an explicit null, at a fraction of the
token cost, so nothing meaningful is lost.
"""

from __future__ import annotations

from typing import Any


def trim_response(data: Any) -> Any:
    if isinstance(data, dict):
        return {k: trim_response(v) for k, v in data.items() if v is not None}
    if isinstance(data, list):
        return [trim_response(v) for v in data]
    return data
