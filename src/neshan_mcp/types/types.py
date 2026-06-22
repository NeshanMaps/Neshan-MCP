"""Shared value types used across schemas and handlers."""

from __future__ import annotations

from typing import Any, TypedDict

from pydantic import BaseModel, Field


class Coordinate(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)

    def as_pair(self) -> list[float]:
        return [self.lat, self.lng]


class ErrorResult(TypedDict):
    error: bool
    status: int | None
    message: str
    hint: str | None


NeshanResponse = dict[str, Any]
