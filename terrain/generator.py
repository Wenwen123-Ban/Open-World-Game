"""Master world generator for noise, biome assignment, and features."""

from __future__ import annotations

from terrain.biome import classify_tile
from terrain.noise_map import NoiseMap
from terrain.tile import Tile


class WorldGenerator:
    """Generate a complete tile grid from deterministic noise maps."""

    def __init__(self, width: int, height: int, seed: int = 1337) -> None:
        self.width = width
        self.height = height
        self.seed = seed
        self.elevation = NoiseMap(seed, scale=88.0, octaves=4)
        self.moisture = NoiseMap(seed + 101, scale=56.0, octaves=3)

    def generate(self) -> list[list[Tile]]:
        """Build a two-dimensional world grid indexed as grid[y][x]."""

        return [[self._make_tile(x, y) for x in range(self.width)] for y in range(self.height)]

    def _make_tile(self, x: int, y: int) -> Tile:
        elevation = self.elevation.sample(x, y)
        moisture = self.moisture.sample(x, y)
        latitude = abs((y / max(1, self.height - 1)) - 0.5) * 2.0
        temperature = max(0.0, min(1.0, 1.0 - latitude - max(0.0, elevation - 0.55) * 0.8))
        return Tile(classify_tile(elevation, moisture, temperature), elevation, moisture, temperature)
