"""Base entity primitives shared by all simulated world actors."""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import count
from math import hypot
from typing import Protocol

import pygame

from settings import TILE_SIZE


class WalkabilityMap(Protocol):
    """Small protocol entities use to query terrain passability."""

    def is_walkable_pixel(self, x: float, y: float) -> bool:
        """Return whether a pixel position can be occupied by an entity."""


_ENTITY_IDS = count(1)


@dataclass(slots=True)
class Entity:
    """A lightweight actor with position, movement, update, and draw hooks."""

    x: float
    y: float
    radius: int = 5
    color: tuple[int, int, int] = (240, 240, 240)
    name: str = "Entity"
    speed: float = 28.0
    entity_id: int = field(default_factory=lambda: next(_ENTITY_IDS), init=False)

    @property
    def tile_pos(self) -> tuple[int, int]:
        """Return the tile coordinate currently occupied by the entity."""

        return int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)

    def update(self, dt: float, world: WalkabilityMap) -> None:
        """Advance behavior for one frame; subclasses can override."""

    def draw(self, screen: pygame.Surface, camera) -> None:
        """Draw the entity as a camera-aware circle marker."""

        screen_x, screen_y = camera.world_to_screen(self.x, self.y)
        scaled_radius = max(2, int(self.radius * camera.zoom))
        pygame.draw.circle(screen, (27, 24, 20), (screen_x, screen_y), scaled_radius + 1)
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), scaled_radius)

    def move_toward(self, target_x: float, target_y: float, dt: float, world: WalkabilityMap) -> bool:
        """Move toward a target, stopping when blocked or reached."""

        dx = target_x - self.x
        dy = target_y - self.y
        distance = hypot(dx, dy)
        if distance <= 0.01:
            return True

        step = min(distance, self.speed * dt)
        next_x = self.x + dx / distance * step
        next_y = self.y + dy / distance * step
        if not world.is_walkable_pixel(next_x, next_y):
            return False

        self.x = next_x
        self.y = next_y
        return step >= distance - 0.01
