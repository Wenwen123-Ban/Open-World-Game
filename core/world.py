"""World grid and chunk loading coordination."""

from __future__ import annotations

import pygame

from core.camera import Camera
from core.chunk import Chunk
from settings import CHUNK_SIZE, TILE_SIZE, WORLD_H, WORLD_W
from terrain.generator import WorldGenerator


class World:
    """Owns terrain tiles, chunk cache, updates, and drawing."""

    def __init__(self, seed: int = 1337) -> None:
        self.width = WORLD_W
        self.height = WORLD_H
        self.tiles = WorldGenerator(self.width, self.height, seed).generate()
        self.chunks: dict[tuple[int, int], Chunk] = {}
        self._build_chunks()

    def draw(self, screen: pygame.Surface, camera: Camera) -> None:
        left, top, right, bottom = camera.visible_tile_bounds()
        chunk_left = left // CHUNK_SIZE
        chunk_top = top // CHUNK_SIZE
        chunk_right = (right // CHUNK_SIZE) + 1
        chunk_bottom = (bottom // CHUNK_SIZE) + 1
        for chunk_y in range(chunk_top, chunk_bottom):
            for chunk_x in range(chunk_left, chunk_right):
                chunk = self.chunks.get((chunk_x, chunk_y))
                if chunk is None:
                    continue
                world_x = chunk_x * CHUNK_SIZE * TILE_SIZE
                world_y = chunk_y * CHUNK_SIZE * TILE_SIZE
                screen_pos = camera.world_to_screen(world_x, world_y)
                size = int(CHUNK_SIZE * TILE_SIZE * camera.zoom)
                surface = pygame.transform.scale(chunk.render_surface(), (size, size))
                screen.blit(surface, screen_pos)

    def _build_chunks(self) -> None:
        for chunk_y in range(0, self.height, CHUNK_SIZE):
            for chunk_x in range(0, self.width, CHUNK_SIZE):
                rows = [row[chunk_x : chunk_x + CHUNK_SIZE] for row in self.tiles[chunk_y : chunk_y + CHUNK_SIZE]]
                self.chunks[(chunk_x // CHUNK_SIZE, chunk_y // CHUNK_SIZE)] = Chunk(
                    chunk_x // CHUNK_SIZE, chunk_y // CHUNK_SIZE, rows
                )
