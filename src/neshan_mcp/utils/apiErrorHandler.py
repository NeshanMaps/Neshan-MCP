"""Centralized API error type, hints, and the handler decorator."""

from __future__ import annotations

import functools
from collections.abc import Awaitable, Callable
from typing import Any

from pydantic import ValidationError

from .logger import get_logger
from .responseTrimmer import trim_response

logger = get_logger("neshan_mcp.errors")

# Documented Neshan error meanings (HTTP status -> hint).
ERROR_HINTS = {
    400: "Invalid request / invalid coordinates.",
    401: "Missing or invalid Api-Key.",
    403: "Key scope mismatch: this key is not authorized for this service.",
    422: "Unprocessable input (bad parameters).",
    429: "Rate limit exceeded (per-minute or quota).",
}


class NeshanError(Exception):
    def __init__(self, status: int | None, message: str, payload: Any = None):
        self.status = status
        self.message = message
        self.payload = payload
        super().__init__(f"[{status}] {message}")

    def as_dict(self) -> dict[str, Any]:
        return {
            "error": True,
            "status": self.status,
            "message": self.message,
            "hint": ERROR_HINTS.get(self.status or 0),
        }


def _validation_dict(message: str) -> dict[str, Any]:
    return {"error": True, "status": None, "message": message, "hint": "Invalid input."}


def handle_api_errors(fn: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    """Wrap a handler so input/API errors become uniform error dicts."""

    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            result = await fn(*args, **kwargs)
            return trim_response(result)
        except ValidationError as e:
            first = e.errors()[0] if e.errors() else {}
            loc = ".".join(str(x) for x in first.get("loc", ()))
            msg = first.get("msg", "invalid input")
            return _validation_dict(f"{loc}: {msg}" if loc else msg)
        except ValueError as e:
            return _validation_dict(str(e))
        except NeshanError as e:
            return e.as_dict()
        except Exception as e:
            logger.exception("unhandled error in %s", fn.__name__)
            return {
                "error": True,
                "status": None,
                "message": f"Internal error: {e}",
                "hint": "This is unexpected — please report it.",
            }

    return wrapper
