"""Tile types, properties, and metadata."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TileType(Enum):
    """Terrain tile identifiers used by the renderer and simulation."""

    DEEP_WATER = "deep_water"
    SHALLOW_WATER = "shallow_water"
    SAND = "sand"
    GRASS = "grass"
    FOREST = "forest"
    HILL = "hill"
    MOUNTAIN = "mountain"
    SNOW = "snow"


@dataclass(frozen=True)
class TileDefinition:
    """Static display and gameplay data for a tile type."""

    name: str
    color: tuple[int, int, int]
    walkable: bool = True
    blocks_sight: bool = False


TILE_DEFINITIONS: dict[TileType, TileDefinition] = {
    TileType.DEEP_WATER: TileDefinition("Deep Water", (19, 64, 130), False),
    TileType.SHALLOW_WATER: TileDefinition("Shallow Water", (42, 120, 175), False),
    TileType.SAND: TileDefinition("Sand", (214, 190, 121)),
    TileType.GRASS: TileDefinition("Grass", (78, 153, 73)),
    TileType.FOREST: TileDefinition("Forest", (38, 105, 55), True, True),
    TileType.HILL: TileDefinition("Hill", (117, 126, 83)),
    TileType.MOUNTAIN: TileDefinition("Mountain", (118, 118, 118), False, True),
    TileType.SNOW: TileDefinition("Snow", (225, 234, 235)),
}


@dataclass(slots=True)
class Tile:
    """A single world tile instance."""

    tile_type: TileType
    elevation: float
    moisture: float
    temperature: float

    @property
    def definition(self) -> TileDefinition:
        """Return immutable metadata for this tile."""

        return TILE_DEFINITIONS[self.tile_type]
