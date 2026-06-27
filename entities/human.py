"""Human villager, settler, warrior, and ruler entities."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from entities.base_entity import Entity, WalkabilityMap
from settings import TILE_SIZE


@dataclass(slots=True)
class Human(Entity):
    """First-pass autonomous human that idles and wanders on walkable land."""

    color: tuple[int, int, int] = (238, 198, 115)
    name: str = "Human"
    speed: float = 34.0
    wander_radius_tiles: int = 7
    _target: tuple[float, float] | None = field(default=None, init=False, repr=False)
    _idle_timer: float = field(default=0.0, init=False, repr=False)

    def update(self, dt: float, world: WalkabilityMap) -> None:
        if self._idle_timer > 0:
            self._idle_timer -= dt
            return

        if self._target is None:
            self._target = self._pick_wander_target(world)
            if self._target is None:
                self._idle_timer = random.uniform(0.5, 1.5)
                return

        reached = self.move_toward(self._target[0], self._target[1], dt, world)
        if reached:
            self._target = None
            self._idle_timer = random.uniform(0.4, 1.2)
        elif not world.is_walkable_pixel(self.x, self.y):
            self._target = None

    def _pick_wander_target(self, world: WalkabilityMap) -> tuple[float, float] | None:
        origin_tile_x, origin_tile_y = self.tile_pos
        for _ in range(12):
            tile_x = origin_tile_x + random.randint(-self.wander_radius_tiles, self.wander_radius_tiles)
            tile_y = origin_tile_y + random.randint(-self.wander_radius_tiles, self.wander_radius_tiles)
            target_x = tile_x * TILE_SIZE + TILE_SIZE / 2
            target_y = tile_y * TILE_SIZE + TILE_SIZE / 2
            if world.is_walkable_pixel(target_x, target_y):
                return target_x, target_y
        return None
