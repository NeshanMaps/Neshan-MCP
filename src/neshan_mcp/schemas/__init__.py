"""Aggregated input schemas (mirrors schemas/index)."""

from .map import StaticMapInput
from .traffic import TrafficAnalyticsInput
from .routing import DirectionInput, HistoricalDirectionInput, IsochroneInput, MapMatchingInput, MatrixInput, TspInput
from .search import GeocodeInput, GeocodePlusInput, ReverseInput, SearchInput
from .zipcode import ZipcodeInput
from .vrp import VRPInput

__all__ = [
    "SearchInput",
    "ReverseInput",
    "GeocodeInput",
    "GeocodePlusInput",
    "DirectionInput",
    "HistoricalDirectionInput",
    "MatrixInput",
    "TspInput",
    "MapMatchingInput",
    "IsochroneInput",
    "StaticMapInput",
    "TrafficAnalyticsInput",
    "ZipcodeInput",
    "VRPInput",
]
