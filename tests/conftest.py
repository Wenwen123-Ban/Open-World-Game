"""Pytest configuration for headless tests without a display server."""

from __future__ import annotations

import os
import sys
import types

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

try:
    import pygame  # noqa: F401
except ModuleNotFoundError:
    pygame_stub = types.ModuleType("pygame")
    pygame_stub.MOUSEWHEEL = 1027
    pygame_stub.K_d = 100
    pygame_stub.K_RIGHT = 1073741903
    pygame_stub.K_a = 97
    pygame_stub.K_LEFT = 1073741904
    pygame_stub.K_s = 115
    pygame_stub.K_DOWN = 1073741905
    pygame_stub.K_w = 119
    pygame_stub.K_UP = 1073741906
    pygame_stub.event = types.SimpleNamespace(Event=object)
    pygame_stub.mouse = types.SimpleNamespace(get_pos=lambda: (0, 0))
    pygame_stub.key = types.SimpleNamespace(get_pressed=lambda: {})
    pygame_stub.draw = types.SimpleNamespace(circle=lambda *args, **kwargs: None, rect=lambda *args, **kwargs: None)
    pygame_stub.transform = types.SimpleNamespace(scale=lambda surface, size: surface)

    class Surface:
        def __init__(self, size: tuple[int, int]) -> None:
            self.size = size

        def blit(self, *args, **kwargs) -> None:
            return None

    class Rect:
        def __init__(self, *args) -> None:
            self.args = args

    pygame_stub.Surface = Surface
    pygame_stub.Rect = Rect
    sys.modules["pygame"] = pygame_stub
