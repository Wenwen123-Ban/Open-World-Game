"""Viewport panning and zoom controller."""

from __future__ import annotations

import pygame

from settings import SCREEN_H, SCREEN_W, TILE_SIZE, WORLD_H, WORLD_W, ZOOM_MAX, ZOOM_MIN


class Camera:
    """Track the visible world rectangle and convert world/screen coordinates."""

    def __init__(self) -> None:
        self.x = (WORLD_W * TILE_SIZE - SCREEN_W) / 2
        self.y = (WORLD_H * TILE_SIZE - SCREEN_H) / 2
        self.zoom = 2.0
        self.pan_speed = 600.0

    @property
    def scaled_tile_size(self) -> int:
        return max(1, int(TILE_SIZE * self.zoom))

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEWHEEL:
            self.zoom_at(event.y * 0.15, pygame.mouse.get_pos())

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        if dx or dy:
            self.x += dx * self.pan_speed * dt / self.zoom
            self.y += dy * self.pan_speed * dt / self.zoom
        self._clamp()

    def zoom_at(self, amount: float, screen_pos: tuple[int, int]) -> None:
        world_x, world_y = self.screen_to_world(screen_pos)
        old_zoom = self.zoom
        self.zoom = max(ZOOM_MIN, min(ZOOM_MAX, self.zoom + amount))
        if self.zoom == old_zoom:
            return
        self.x = world_x - screen_pos[0] / self.zoom
        self.y = world_y - screen_pos[1] / self.zoom
        self._clamp()

    def screen_to_world(self, pos: tuple[int, int]) -> tuple[float, float]:
        return self.x + pos[0] / self.zoom, self.y + pos[1] / self.zoom

    def world_to_screen(self, x: float, y: float) -> tuple[int, int]:
        return int((x - self.x) * self.zoom), int((y - self.y) * self.zoom)

    def visible_tile_bounds(self) -> tuple[int, int, int, int]:
        left = max(0, int(self.x // TILE_SIZE))
        top = max(0, int(self.y // TILE_SIZE))
        right = min(WORLD_W, int((self.x + SCREEN_W / self.zoom) // TILE_SIZE) + 2)
        bottom = min(WORLD_H, int((self.y + SCREEN_H / self.zoom) // TILE_SIZE) + 2)
        return left, top, right, bottom

    def _clamp(self) -> None:
        max_x = max(0, WORLD_W * TILE_SIZE - SCREEN_W / self.zoom)
        max_y = max(0, WORLD_H * TILE_SIZE - SCREEN_H / self.zoom)
        self.x = max(0, min(max_x, self.x))
        self.y = max(0, min(max_y, self.y))
