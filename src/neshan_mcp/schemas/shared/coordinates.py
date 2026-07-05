"""Shared latitude/longitude constraints.

Reused in both Pydantic input schemas and MCP tool signatures so the bounds
reach the JSON schema an agent sees before calling a tool, not just the
validation error it gets back after.
"""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

Latitude = Annotated[float, Field(ge=-90, le=90)]
Longitude = Annotated[float, Field(ge=-180, le=180)]
