# Architecture Notes

## Initial Direction
- The project is organized around a small Pygame engine with separate packages for core loop systems, terrain generation, entities, gameplay systems, UI, and visual effects.
- World simulation should use chunk-based loading and dirty chunk rendering to keep a 512×512 tile world performant.
- Documentation and session tracking live in `Readme/`; no game code should be placed there.


## Entity System Foundation
- `World` now owns an `EntityManager` alongside terrain chunks, so simulation updates run before drawing and entities render above terrain.
- Entities use pixel-space positions for smooth movement and expose tile coordinates for terrain-aware decisions.
- Terrain passability is accessed through `World.is_walkable_tile` and `World.is_walkable_pixel`, keeping behavior code independent from tile storage details.
- The first concrete behavior is `Human`, an autonomous wanderer that chooses nearby walkable targets and idles between moves.
