"""Entity tracking, update, and rendering coordination."""

from __future__ import annotations

from collections.abc import Iterable

import pygame

from entities.base_entity import Entity, WalkabilityMap


class EntityManager:
    """Owns active entities and updates/draws them in a stable order."""

    def __init__(self, entities: Iterable[Entity] = ()) -> None:
        self.entities: list[Entity] = list(entities)

    def add(self, entity: Entity) -> Entity:
        """Register an entity and return it for caller convenience."""

        self.entities.append(entity)
        return entity

    def update(self, dt: float, world: WalkabilityMap) -> None:
        """Update all active entities."""

        for entity in self.entities:
            entity.update(dt, world)

    def draw(self, screen: pygame.Surface, camera) -> None:
        """Draw entities sorted by y-position for simple depth ordering."""

        for entity in sorted(self.entities, key=lambda item: item.y):
            entity.draw(screen, camera)

    def __len__(self) -> int:
        return len(self.entities)
