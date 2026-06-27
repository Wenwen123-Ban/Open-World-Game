"""Tests for deterministic terrain generation and biome rules."""

from __future__ import annotations

from terrain.biome import classify_tile
from terrain.generator import WorldGenerator
from terrain.tile import TileType


def test_world_generator_is_deterministic_for_same_seed() -> None:
    first = WorldGenerator(24, 18, seed=2026).generate()
    second = WorldGenerator(24, 18, seed=2026).generate()

    first_signature = [[tile.tile_type for tile in row] for row in first]
    second_signature = [[tile.tile_type for tile in row] for row in second]

    assert first_signature == second_signature


def test_world_generator_produces_expected_dimensions_and_normalized_values() -> None:
    width = 17
    height = 11
    grid = WorldGenerator(width, height, seed=7).generate()

    assert len(grid) == height
    assert all(len(row) == width for row in grid)
    assert all(0.0 <= tile.elevation <= 1.0 for row in grid for tile in row)
    assert all(0.0 <= tile.moisture <= 1.0 for row in grid for tile in row)
    assert all(0.0 <= tile.temperature <= 1.0 for row in grid for tile in row)


def test_biome_thresholds_cover_core_tile_types() -> None:
    assert classify_tile(elevation=0.20, moisture=0.50, temperature=0.50) is TileType.DEEP_WATER
    assert classify_tile(elevation=0.32, moisture=0.50, temperature=0.50) is TileType.SHALLOW_WATER
    assert classify_tile(elevation=0.37, moisture=0.50, temperature=0.50) is TileType.SAND
    assert classify_tile(elevation=0.85, moisture=0.50, temperature=0.70) is TileType.MOUNTAIN
    assert classify_tile(elevation=0.85, moisture=0.50, temperature=0.20) is TileType.SNOW
    assert classify_tile(elevation=0.50, moisture=0.75, temperature=0.50) is TileType.FOREST
