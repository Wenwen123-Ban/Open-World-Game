# Architecture Notes

## Initial Direction
- The project is organized around a small Pygame engine with separate packages for core loop systems, terrain generation, entities, gameplay systems, UI, and visual effects.
- World simulation should use chunk-based loading and dirty chunk rendering to keep a 512×512 tile world performant.
- Documentation and session tracking live in `Readme/`; no game code should be placed there.
