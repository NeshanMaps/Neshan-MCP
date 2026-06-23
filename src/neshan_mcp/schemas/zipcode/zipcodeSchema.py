"""Input schema for the zipcode domain."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ZipcodeInput(BaseModel):
    zipcode: str = Field(description="10-digit Iranian postal code.")
