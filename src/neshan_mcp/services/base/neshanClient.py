"""Shared async HTTP client for the Neshan REST API (base service)."""

from __future__ import annotations

import asyncio
from typing import Any

import httpx

from ...appConfig import settings
from ...auth import resolve_key
from ...utils import NeshanError, get_logger

logger = get_logger("neshan_mcp.http")

_MAX_RETRY_AFTER = 5.0  # cap on server-supplied Retry-After so a tool call can't hang indefinitely


class NeshanClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=settings.base_url,
            timeout=settings.timeout,
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def get_json(self, path: str, *, service: str, params: dict[str, Any]) -> Any:
        return await self._request(path, service=service, params=params)

    async def get_bytes_with_query_key(
        self, path: str, *, service: str, params: dict[str, Any]
    ) -> bytes:
        return await self._request(
            path, service=service, params=params, key_in_query=True, expect_json=False
        )

    async def get_bytes(self, path: str, *, service: str) -> bytes:
        """GET a binary resource at *path* using the standard Api-Key header."""
        return await self._request(path, service=service, params={}, expect_json=False)

    async def post_json(self, path: str, *, service: str, body: dict[str, Any]) -> Any:
        """POST JSON *body* and return parsed JSON response."""
        return await self._request(path, service=service, params={}, body=body)

    async def _request(
        self,
        path: str,
        *,
        service: str,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        key_in_query: bool = False,
        expect_json: bool = True,
    ) -> Any:
        key = resolve_key(service)
        if not key:
            raise NeshanError(
                None,
                "No API key found. Send it in the 'Neshan-Api-Key' request header "
                "(HTTP mode) or set NESHAN_API_KEY in the environment (stdio mode).",
            )

        headers: dict[str, str] = {"Accept": "application/json" if expect_json else "*/*"}
        params = {k: v for k, v in (params or {}).items() if v is not None}
        if key_in_query:
            params["key"] = key
        else:
            headers["Api-Key"] = key

        last_exc: Exception | None = None
        for attempt in range(settings.max_retries + 1):
            try:
                if body is not None:
                    resp = await self._client.post(path, params=params, json=body, headers=headers)
                else:
                    resp = await self._client.get(path, params=params, headers=headers)
            except httpx.RequestError as exc:
                last_exc = exc
                logger.warning("network error on %s (attempt %d): %s", path, attempt, exc)
                await asyncio.sleep(0.4 * (attempt + 1))
                continue

            if resp.status_code >= 500 and attempt < settings.max_retries:
                logger.warning("5xx on %s (attempt %d): %s", path, attempt, resp.status_code)
                await asyncio.sleep(0.4 * (attempt + 1))
                continue

            if resp.status_code == 429 and attempt < settings.max_retries:
                retry_after = _retry_after_seconds(resp.headers.get("Retry-After"))
                delay = min(retry_after, _MAX_RETRY_AFTER) if retry_after is not None else 0.8 * (attempt + 1)
                logger.warning("429 on %s (attempt %d): backing off %.1fs", path, attempt, delay)
                await asyncio.sleep(delay)
                continue

            if resp.status_code >= 400:
                raise NeshanError(resp.status_code, _message_of(resp), _safe_json(resp))

            return resp.json() if expect_json else resp.content

        raise NeshanError(None, f"Network failure after retries: {last_exc}")


def _retry_after_seconds(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None  # Retry-After as an HTTP date isn't parsed; fall back to the default backoff.


def _safe_json(resp: httpx.Response) -> Any:
    try:
        return resp.json()
    except Exception:
        return None


def _message_of(resp: httpx.Response) -> str:
    data = _safe_json(resp)
    if isinstance(data, dict):
        for field in ("message", "msg", "error", "detail"):
            if data.get(field):
                return str(data[field])
    return resp.text[:200] or f"HTTP {resp.status_code}"
