"""Handler for the interactive map view tool."""

from __future__ import annotations

import os
import tempfile
import uuid
from typing import Any

from ..schemas.mapview import MapViewInput, MarkerInput, RouteInput
from ..services.mapview import generate_map_html
from ..utils import handle_api_errors, get_logger

logger = get_logger("neshan_mcp.mapview")

_OUTPUT_DIR = os.environ.get("NESHAN_MAP_OUTPUT_DIR", tempfile.gettempdir())


@handle_api_errors
async def handle_map_view(
    center_lat: float,
    center_lng: float,
    zoom: int,
    markers: list[MarkerInput] | None,
    routes: list[RouteInput] | None,
    title: str,
    show_traffic: bool,
    show_poi: bool,
    map_key: str,
) -> dict[str, Any]:

    data = MapViewInput(
        center_lat=center_lat,
        center_lng=center_lng,
        zoom=zoom,
        markers=markers or [],
        routes=routes or [],
        title=title,
        show_traffic=show_traffic,
        show_poi=show_poi,
        map_key=map_key,
    )

    html = generate_map_html(data)

    filename = f"neshan_map_{uuid.uuid4().hex}.html"
    filepath = os.path.join(_OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    logger.info("map html saved to %s", filepath)

    return {
        "status": "ok",
        "file_path": filepath,
        "message": f"نقشه interactive در {filepath} ذخیره شد. آن را در مرورگر باز کنید.",
        "markers_count": len(data.markers),
        "routes_count": len(data.routes),
        "note": (
            "برای نمایش نقشه پایه نشان، باید map_key (کلید Web SDK نشان) را وارد کنید. "
            "بدون آن، نقشه پایه نشان لود نمی‌شود ولی markers و مسیرها نمایش داده می‌شوند."
            if not map_key else ""
        ),
    }
