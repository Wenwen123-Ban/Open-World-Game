"""Deterministic layered value-noise map wrapper."""

from __future__ import annotations

import math
import random


def _smoothstep(value: float) -> float:
    return value * value * (3.0 - 2.0 * value)


class NoiseMap:
    """Small dependency-light noise helper for early terrain generation."""

    def __init__(self, seed: int, scale: float = 64.0, octaves: int = 3) -> None:
        self.seed = seed
        self.scale = scale
        self.octaves = octaves

    def sample(self, x: int, y: int) -> float:
        """Return a normalized 0..1 noise value for a tile coordinate."""

        total = 0.0
        amplitude = 1.0
        frequency = 1.0
        max_value = 0.0
        for octave in range(self.octaves):
            total += self._value_noise(x / self.scale * frequency, y / self.scale * frequency, octave) * amplitude
            max_value += amplitude
            amplitude *= 0.5
            frequency *= 2.0
        return max(0.0, min(1.0, total / max_value))

    def _corner(self, grid_x: int, grid_y: int, octave: int) -> float:
        rng = random.Random((grid_x * 73856093) ^ (grid_y * 19349663) ^ (self.seed * 83492791) ^ octave)
        return rng.random()

    def _value_noise(self, x: float, y: float, octave: int) -> float:
        x0 = math.floor(x)
        y0 = math.floor(y)
        tx = _smoothstep(x - x0)
        ty = _smoothstep(y - y0)
        v00 = self._corner(x0, y0, octave)
        v10 = self._corner(x0 + 1, y0, octave)
        v01 = self._corner(x0, y0 + 1, octave)
        v11 = self._corner(x0 + 1, y0 + 1, octave)
        top = v00 + (v10 - v00) * tx
        bottom = v01 + (v11 - v01) * tx
        return top + (bottom - top) * ty
