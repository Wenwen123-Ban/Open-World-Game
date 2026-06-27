"""Biome classification logic."""

from __future__ import annotations

from terrain.tile import TileType


def classify_tile(elevation: float, moisture: float, temperature: float) -> TileType:
    """Map generated climate values to a first-pass terrain tile."""

    if elevation < 0.28:
        return TileType.DEEP_WATER
    if elevation < 0.35:
        return TileType.SHALLOW_WATER
    if elevation < 0.39:
        return TileType.SAND
    if elevation > 0.82:
        return TileType.SNOW if temperature < 0.42 else TileType.MOUNTAIN
    if elevation > 0.70:
        return TileType.HILL
    if temperature < 0.22:
        return TileType.SNOW
    if moisture > 0.62:
        return TileType.FOREST
    if moisture < 0.25 and temperature > 0.45:
        return TileType.SAND
    return TileType.GRASS
