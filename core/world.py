"""World grid and chunk loading coordination."""

from __future__ import annotations

import random

import pygame

from core.camera import Camera
from core.chunk import Chunk
from entities.entity_manager import EntityManager
from entities.human import Human
from settings import CHUNK_SIZE, TILE_SIZE, WORLD_H, WORLD_W
from terrain.generator import WorldGenerator


class World:
    """Owns terrain tiles, chunk cache, updates, and drawing."""

    def __init__(self, seed: int = 1337) -> None:
        self.width = WORLD_W
        self.height = WORLD_H
        self.tiles = WorldGenerator(self.width, self.height, seed).generate()
        self.chunks: dict[tuple[int, int], Chunk] = {}
        self.entities = EntityManager()
        self._build_chunks()
        self._spawn_starting_humans(seed)

    def update(self, dt: float) -> None:
        """Advance world simulation systems."""

        self.entities.update(dt, self)

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
        self.entities.draw(screen, camera)

    def is_walkable_tile(self, tile_x: int, tile_y: int) -> bool:
        """Return whether a tile coordinate is inside the world and passable."""

        if not (0 <= tile_x < self.width and 0 <= tile_y < self.height):
            return False
        return self.tiles[tile_y][tile_x].definition.walkable

    def is_walkable_pixel(self, x: float, y: float) -> bool:
        """Return whether a pixel coordinate maps to a passable tile."""

        return self.is_walkable_tile(int(x // TILE_SIZE), int(y // TILE_SIZE))

    def _build_chunks(self) -> None:
        for chunk_y in range(0, self.height, CHUNK_SIZE):
            for chunk_x in range(0, self.width, CHUNK_SIZE):
                rows = [row[chunk_x : chunk_x + CHUNK_SIZE] for row in self.tiles[chunk_y : chunk_y + CHUNK_SIZE]]
                self.chunks[(chunk_x // CHUNK_SIZE, chunk_y // CHUNK_SIZE)] = Chunk(
                    chunk_x // CHUNK_SIZE, chunk_y // CHUNK_SIZE, rows
                )

    def _spawn_starting_humans(self, seed: int, count: int = 24) -> None:
        """Place a small initial population on random walkable tiles."""

        rng = random.Random(seed + 1000)
        attempts = 0
        while len(self.entities) < count and attempts < count * 200:
            attempts += 1
            tile_x = rng.randrange(self.width)
            tile_y = rng.randrange(self.height)
            if not self.is_walkable_tile(tile_x, tile_y):
                continue
            self.entities.add(Human(tile_x * TILE_SIZE + TILE_SIZE / 2, tile_y * TILE_SIZE + TILE_SIZE / 2))
