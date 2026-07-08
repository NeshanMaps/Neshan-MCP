"""Pure URL builders for Neshan app deeplinks — no HTTP calls, no side effects."""

from __future__ import annotations

_WEB_BASE = "https://nshn.ir"

# Only car and motorcycle are supported on Android/Web; iOS supports all five below.
_AW_VEHICLE: dict[str, str] = {"car": "d", "motorcycle": "m"}

_IOS_VEHICLE: dict[str, str] = {
    "car": "d",
    "motorcycle": "m",
    "pedestrian": "w",
    "bicycle": "b",
    "transit": "p",
}


def point_links(lat: float, lng: float) -> dict[str, str]:
    """Return Android/Web and iOS deeplinks for showing a coordinate on the map."""
    return {
        "android_web": f"{_WEB_BASE}/?lat={lat}&lng={lng}",
        "ios": f"neshan://?ll={lat},{lng}",
    }


def routing_links(
    origin_lat: float,
    origin_lng: float,
    dest_lat: float,
    dest_lng: float,
    vehicle: str = "car",
) -> dict[str, str]:
    """Return Android/Web and iOS deeplinks for turn-by-turn navigation."""
    origin = f"{origin_lat},{origin_lng}"
    dest = f"{dest_lat},{dest_lng}"
    aw_v = _AW_VEHICLE.get(vehicle, "d")
    ios_v = _IOS_VEHICLE.get(vehicle, "d")
    return {
        "android_web": f"{_WEB_BASE}?origin={origin}&destination={dest}&vehicle={aw_v}",
        "ios": f"neshan://?origin={origin}&destination={dest}&vehicle={ios_v}",
    }
