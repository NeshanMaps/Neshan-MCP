"""Input schema for the point domain."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PointInput(BaseModel):
    hash: str = Field(min_length=1)
