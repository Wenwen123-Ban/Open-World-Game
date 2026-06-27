"""Tests for entity movement and walkability constraints."""

from __future__ import annotations

from entities.base_entity import Entity


class StubWorld:
    def __init__(self, blocked_after_x: float | None = None) -> None:
        self.blocked_after_x = blocked_after_x

    def is_walkable_pixel(self, x: float, y: float) -> bool:
        return self.blocked_after_x is None or x <= self.blocked_after_x


def test_entity_move_toward_reaches_target_without_overshooting() -> None:
    entity = Entity(0.0, 0.0, speed=10.0)

    reached = entity.move_toward(6.0, 8.0, dt=2.0, world=StubWorld())

    assert reached is True
    assert entity.x == 6.0
    assert entity.y == 8.0


def test_entity_move_toward_stops_before_blocked_tile() -> None:
    entity = Entity(0.0, 0.0, speed=10.0)

    reached = entity.move_toward(20.0, 0.0, dt=1.0, world=StubWorld(blocked_after_x=5.0))

    assert reached is False
    assert entity.x == 0.0
    assert entity.y == 0.0
