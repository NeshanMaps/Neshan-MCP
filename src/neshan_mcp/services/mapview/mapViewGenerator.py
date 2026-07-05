"""HTML generator for the interactive Neshan map view."""

from __future__ import annotations

import html
import json
import math

from ...schemas.mapview import MapViewInput
from ...utils import get_logger

logger = get_logger("neshan_mcp.mapview")

# CDN رسمی نشان (از README پکیج)
_SDK_CSS = "https://static.neshan.org/sdk/mapboxgl/v1.13.2/neshan-sdk/v1.1.3/index.css"
_SDK_JS  = "https://static.neshan.org/sdk/mapboxgl/v1.13.2/neshan-sdk/v1.1.3/index.js"


def _js_string(value: str) -> str:
    """JSON-encode a string for embedding inside an inline <script> block.

    json.dumps alone escapes JS syntax but not HTML: a literal '</script>'
    substring inside the resulting string is still recognized by the HTML
    tokenizer as closing the surrounding <script> tag, regardless of JS-level
    quoting. Escaping the slash defuses that without changing the decoded
    JS string value.
    """
    return json.dumps(value).replace("</", "<\\/")


# ---- polyline decoder (Google/Neshan encoded polyline) ----

def _decode_polyline(encoded: str) -> list[list[float]]:
    """Decode Google encoded polyline to [[lat, lng], ...] list."""
    coords: list[list[float]] = []
    index = 0
    lat = 0
    lng = 0
    while index < len(encoded):
        for is_lng in (False, True):
            result = 0
            shift = 0
            while True:
                b = ord(encoded[index]) - 63
                index += 1
                result |= (b & 0x1F) << shift
                shift += 5
                if b < 0x20:
                    break
            delta = ~(result >> 1) if result & 1 else result >> 1
            if is_lng:
                lng += delta
            else:
                lat += delta
        coords.append([lat / 1e5, lng / 1e5])
    return coords


def _auto_center(data: MapViewInput) -> tuple[float, float, int]:
    """مرکز و zoom رو از مجموع همه نقاط حساب کن."""
    all_points: list[tuple[float, float]] = []

    for m in data.markers:
        all_points.append((m.lat, m.lng))

    for i, r in enumerate(data.routes):
        if r.encoded_polyline:
            try:
                pts = _decode_polyline(r.encoded_polyline)
                all_points.extend((p[0], p[1]) for p in pts)
            except Exception:
                logger.warning("failed to decode encoded_polyline for route %d; excluded from auto-center", i)
        elif r.coordinates:
            all_points.extend((p[0], p[1]) for p in r.coordinates)

    if not all_points:
        return data.center_lat, data.center_lng, data.zoom

    min_lat = min(p[0] for p in all_points)
    max_lat = max(p[0] for p in all_points)
    min_lng = min(p[1] for p in all_points)
    max_lng = max(p[1] for p in all_points)

    center_lat = (min_lat + max_lat) / 2
    center_lng = (min_lng + max_lng) / 2

    # تخمین zoom بر اساس bbox
    lat_span = max(max_lat - min_lat, 0.001)
    lng_span = max(max_lng - min_lng, 0.001)
    span = max(lat_span, lng_span)
    zoom = max(2, min(16, int(math.log2(360 / span)) - 1))

    return center_lat, center_lng, zoom


def _build_markers_js(data: MapViewInput) -> str:
    if not data.markers:
        return ""
    lines = []
    for m in data.markers:
        label_html = (
            f"<b>{html.escape(m.label)}</b><br/>{m.lat:.6f}, {m.lng:.6f}"
            if m.label else f"{m.lat:.6f}, {m.lng:.6f}"
        )
        lines.append(f"""
    new nmp_mapboxgl.Marker({{ color: {_js_string(m.color)} }})
        .setLngLat([{m.lng}, {m.lat}])
        .setPopup(new nmp_mapboxgl.Popup({{ offset: 25 }}).setHTML({_js_string(label_html)}))
        .addTo(map);""")
    return "\n".join(lines)


def _build_routes_js(data: MapViewInput) -> str:
    if not data.routes:
        return ""
    lines = []
    for i, r in enumerate(data.routes):
        coords: list[list[float]] = []
        if r.encoded_polyline:
            try:
                pts = _decode_polyline(r.encoded_polyline)
                coords = [[p[1], p[0]] for p in pts]  # [lng, lat] برای mapbox
            except Exception:
                logger.warning("failed to decode encoded_polyline for route %d; route skipped", i)
        elif r.coordinates:
            coords = [[p[1], p[0]] for p in r.coordinates]  # [lng, lat]

        if not coords:
            continue

        coords_json = json.dumps(coords)
        source_id = f"route-source-{i}"
        layer_id = f"route-layer-{i}"
        label = r.label or f"مسیر {i+1}"

        lines.append(f"""
    map.addSource('{source_id}', {{
        type: 'geojson',
        data: {{
            type: 'Feature',
            properties: {{ label: {_js_string(label)} }},
            geometry: {{ type: 'LineString', coordinates: {coords_json} }}
        }}
    }});
    map.addLayer({{
        id: '{layer_id}',
        type: 'line',
        source: '{source_id}',
        layout: {{ 'line-join': 'round', 'line-cap': 'round' }},
        paint: {{ 'line-color': {_js_string(r.color)}, 'line-width': 5, 'line-opacity': 0.85 }}
    }});""")
    return "\n".join(lines)


def generate_map_html(data: MapViewInput) -> str:
    """تولید HTML کامل نقشه interactive نشان."""

    if data.markers or data.routes:
        center_lat, center_lng, zoom = _auto_center(data)
    else:
        center_lat, center_lng, zoom = data.center_lat, data.center_lng, data.zoom

    markers_js = _build_markers_js(data)
    routes_js = _build_routes_js(data)
    has_routes = bool(data.routes and routes_js.strip())

    map_key = data.map_key or "YOUR_WEB_MAP_KEY"
    title_html = html.escape(data.title)
    traffic_str = "true" if data.show_traffic else "false"
    poi_str = "true" if data.show_poi else "false"

    routes_on_load = f"""
    map.on('load', function() {{
        {routes_js}
    }});""" if has_routes else ""

    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title_html}</title>
<link rel="stylesheet" href="{_SDK_CSS}"/>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: Tahoma, sans-serif; height: 100vh; display: flex; flex-direction: column; background: #1a1a2e; }}
  #header {{
    padding: 10px 16px;
    background: #16213e;
    color: #e0e0e0;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
    border-bottom: 2px solid #0f3460;
  }}
  #header .logo {{ font-weight: bold; font-size: 16px; color: #4fc3f7; }}
  #header .title {{ flex: 1; }}
  #map {{ flex: 1; width: 100%; }}
  .mapboxgl-popup-content {{ font-family: Tahoma, sans-serif; font-size: 13px; direction: rtl; }}
</style>
</head>
<body>
<div id="header">
  <span class="logo">نشان</span>
  <span class="title">{title_html}</span>
</div>
<div id="map"></div>
<script src="{_SDK_JS}"></script>
<script>
var map = new nmp_mapboxgl.Map({{
    mapType: nmp_mapboxgl.Map.mapTypes.neshanVector,
    container: 'map',
    zoom: {zoom},
    center: [{center_lng}, {center_lat}],
    minZoom: 2,
    maxZoom: 21,
    trackResize: true,
    mapKey: {_js_string(map_key)},
    poi: {poi_str},
    traffic: {traffic_str},
}});

map.addControl(new nmp_mapboxgl.NavigationControl(), 'top-left');
map.addControl(new nmp_mapboxgl.FullscreenControl(), 'top-left');
map.addControl(new nmp_mapboxgl.GeolocateControl({{
    positionOptions: {{ enableHighAccuracy: true }},
    trackUserLocation: true
}}), 'top-left');

{markers_js}
{routes_on_load}
</script>
</body>
</html>"""
