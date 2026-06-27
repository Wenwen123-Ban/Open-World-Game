"""Main game loop and event dispatch orchestration."""

from __future__ import annotations

import pygame

from core.camera import Camera
from core.world import World
from settings import FPS, SCREEN_H, SCREEN_W


class Game:
    """Phase 0 game foundation: window, loop, camera, and terrain rendering."""

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Open World Game — Phase 0 Foundation")
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 18)
        self.camera = Camera()
        self.world = World()
        self.running = True

    def run(self) -> None:
        """Run until the player closes the window or presses Escape."""

        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self._handle_events()
            self.camera.update(dt)
            self.world.update(dt)
            self._draw()
        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            else:
                self.camera.handle_event(event)

    def _draw(self) -> None:
        self.screen.fill((12, 18, 30))
        self.world.draw(self.screen, self.camera)
        self._draw_hud()
        pygame.display.flip()

    def _draw_hud(self) -> None:
        lines = [
            "WASD/Arrows: pan  Mouse wheel: zoom  Esc: quit",
            f"Camera=({self.camera.x:.0f}, {self.camera.y:.0f}) Zoom={self.camera.zoom:.2f} FPS={self.clock.get_fps():.0f}",
            f"Entities={len(self.world.entities)} Humans wandering on walkable land",
        ]
        for index, text in enumerate(lines):
            surface = self.font.render(text, True, (235, 226, 190))
            self.screen.blit(surface, (12, 12 + index * 22))
