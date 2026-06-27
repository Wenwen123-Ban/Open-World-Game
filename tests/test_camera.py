"""Tests for camera coordinate conversions and zoom behavior."""

from __future__ import annotations

from core.camera import Camera


def test_camera_screen_world_round_trip() -> None:
    camera = Camera()
    camera.x = 128.5
    camera.y = 64.25
    camera.zoom = 2.5

    world_pos = camera.screen_to_world((320, 180))

    assert camera.world_to_screen(*world_pos) == (320, 180)


def test_camera_zoom_at_keeps_cursor_world_position_stable() -> None:
    camera = Camera()
    camera.x = 100.0
    camera.y = 200.0
    camera.zoom = 2.0
    cursor = (400, 250)
    before = camera.screen_to_world(cursor)

    camera.zoom_at(1.0, cursor)

    after = camera.screen_to_world(cursor)
    assert after == before
