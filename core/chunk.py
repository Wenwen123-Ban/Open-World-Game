"""Individual chunk data and rendering helpers."""

from __future__ import annotations

import pygame

from settings import CHUNK_SIZE, TILE_SIZE
from terrain.tile import Tile, TILE_DEFINITIONS


class Chunk:
    """A cached square block of tiles."""

    def __init__(self, chunk_x: int, chunk_y: int, tiles: list[list[Tile]]) -> None:
        self.chunk_x = chunk_x
        self.chunk_y = chunk_y
        self.tiles = tiles
        self.dirty = True
        self.surface = pygame.Surface((CHUNK_SIZE * TILE_SIZE, CHUNK_SIZE * TILE_SIZE))

    def render_surface(self) -> pygame.Surface:
        if self.dirty:
            for row_index, row in enumerate(self.tiles):
                for col_index, tile in enumerate(row):
                    color = TILE_DEFINITIONS[tile.tile_type].color
                    rect = pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(self.surface, color, rect)
            self.dirty = False
        return self.surface
