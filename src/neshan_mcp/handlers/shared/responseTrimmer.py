"""Response shaping shared by handlers.

Hook for trimming verbose API responses before they reach the model. Kept
conservative: only strips top-level null fields so nothing meaningful is lost.
"""

from __future__ import annotations

from typing import Any


def trim_response(data: Any) -> Any:
    if isinstance(data, dict):
        return {k: v for k, v in data.items() if v is not None}
    return data
