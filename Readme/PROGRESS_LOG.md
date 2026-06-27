# Progress Log

## 2026-06-27 — Project Foundation
**Duration:** Initial setup

**What was done:**
- Stored the full game design plan in `Readme/GAME_DESIGN_PLAN.md`.
- Created the initial project folder structure for core engine, terrain, entities, systems, UI, effects, and reusable graphics assets.
- Added lightweight placeholder Python modules for planned systems.

**Decisions made:**
- Use Pygame with 16×16 base tiles, 16×16 chunks, and a 512×512 default world.
- Keep progress and planning documentation in the `Readme/` folder only.

**Next session goal:**
- Implement Phase 0 foundation: Pygame window, game loop, FPS cap, camera, and basic chunk/tile rendering.

## 2026-06-27 — Phase 0 Playable Terrain Foundation
**Duration:** ~1 hour

**What was done:**
- Replaced the placeholder entry point with a runnable Pygame application.
- Added the first `Game` loop with FPS cap, close/Escape handling, terrain drawing, and simple debug HUD text.
- Implemented a camera that supports keyboard panning, mouse-wheel zooming, coordinate conversion, and world bounds clamping.
- Implemented deterministic first-pass world generation from layered value noise plus biome classification.
- Added tile definitions and cached chunk rendering so the visible world can be drawn efficiently.

**Decisions made:**
- Use an internal deterministic value-noise helper for the first playable foundation so terrain generation works even before tuning external noise-library usage.
- Keep the first visible game base focused on Phase 0: window, loop, camera, generated terrain, and chunk rendering before adding entities or powers.
- Use simple colored rectangles for terrain now; art assets and tile variants can replace the cached chunk surfaces later without changing the high-level world flow.

**Next session goal:**
- Add a small entity foundation: base entity class, entity manager, human wander behavior, and rendering on top of the terrain.

## 2026-06-27 — Phase 1 Entity Foundation
**Duration:** ~45 minutes

**What was done:**
- Added a shared base entity with id assignment, tile-position helpers, movement toward targets, and camera-aware circle rendering.
- Added an entity manager that owns active entities, updates them each frame, and draws them with simple y-depth ordering.
- Implemented first-pass human behavior: humans idle briefly, pick nearby walkable wander targets, and move only across passable terrain.
- Integrated entities into the world update/draw path and seeded a small starting human population on walkable tiles.
- Extended the debug HUD with a live entity count.

**Decisions made:**
- Keep Phase 1 visuals as simple circles so behavior and simulation plumbing can be validated before sprite work.
- Let entities query the world through small walkability helpers instead of directly coupling behavior to terrain internals.
- Use deterministic world-seeded initial placement while allowing moment-to-moment wander timing to feel organic.

**Next session goal:**
- Expand entity variety with animals/monsters or begin simple needs/faction hooks for human civilization behavior.
