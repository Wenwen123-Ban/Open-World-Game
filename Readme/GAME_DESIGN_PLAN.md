# 🌍 Open World Game — Full Design Plan
**Engine:** Pygame (Python) | **Style:** 2D Pixel Art | **Inspired By:** WorldBox Sandbox
**Project Root:** `Open World Game/`

---

## 📁 Project Folder Structure

```
Open World Game/
│
├── main.py                        # Entry point
├── settings.py                    # Global constants (tile size, FPS, screen size, etc.)
├── requirements.txt               # pygame, noise, etc.
│
├── core/                          # Core engine systems
│   ├── game.py                    # Main game loop, event dispatch
│   ├── camera.py                  # Viewport / pan / zoom controller
│   ├── world.py                   # World grid, chunk loader
│   ├── chunk.py                   # Individual chunk data and rendering
│   ├── clock.py                   # In-game time (day/night, seasons)
│   └── event_bus.py               # Decoupled event messaging system
│
├── terrain/                       # World generation
│   ├── generator.py               # Master generator (calls noise, biome, etc.)
│   ├── noise_map.py               # Perlin/Simplex noise wrapper
│   ├── biome.py                   # Biome classification logic
│   └── tile.py                    # Tile types, properties, metadata
│
├── entities/                      # Living beings & objects
│   ├── base_entity.py             # Abstract entity class
│   ├── human.py                   # Human villager, settler, warrior, king
│   ├── animal.py                  # Deer, wolf, bear, fish, birds, etc.
│   ├── monster.py                 # Goblin, orc, dragon, undead, demon
│   ├── npc_faction.py             # Faction/kingdom system
│   └── entity_manager.py         # Tracks + updates all entities
│
├── systems/                       # ECS-like gameplay systems
│   ├── ai_system.py               # Behavior trees / state machines for entities
│   ├── combat_system.py           # Damage, death, loot
│   ├── civilization_system.py     # Building cities, tech tree, wars
│   ├── weather_system.py          # Rain, snow, storms, drought
│   ├── disaster_system.py         # Earthquakes, floods, plagues, meteor strikes
│   ├── magic_system.py            # God powers, spell effects
│   ├── trade_system.py            # Between civilizations
│   ├── migration_system.py        # Population spread, colonization
│   └── ecology_system.py          # Food chains, animal populations
│
├── ui/                            # All HUD and interface
│   ├── hud.py                     # Top/bottom HUD bar
│   ├── toolbar.py                 # God power selector
│   ├── tooltip.py                 # Hover-over info boxes
│   ├── minimap.py                 # Live minimap
│   ├── panel_info.py              # Entity inspector panel
│   └── menu.py                    # Main menu, pause screen
│
├── effects/                       # Visual FX
│   ├── particle_system.py         # General particle engine
│   ├── fire_effect.py             # Flame + ember particles
│   ├── rain_effect.py             # Raindrop streaks
│   ├── snow_effect.py             # Snowflake particles
│   ├── explosion_effect.py        # Shockwave + debris
│   ├── magic_effect.py            # Glow, beam, ripple effects
│   ├── blood_effect.py            # Combat splatter
│   └── ambient_particles.py       # Leaves, dust, butterflies
│
├── Graphics/
│   └── Reusables/                 # All downloaded or created art assets
│       ├── tiles/                 # Terrain tiles (grass, sand, water, snow, etc.)
│       ├── entities/              # Entity spritesheets
│       │   ├── humans/
│       │   ├── animals/
│       │   └── monsters/
│       ├── buildings/             # Hut, house, castle, farm, church, etc.
│       ├── ui/                    # Buttons, panels, icons, cursor
│       ├── effects/               # Flame sheets, explosion frames, ripple PNGs
│       └── world/                 # Trees, rocks, mountains, ores, ruins
│
└── Readme/                        # Progress tracker (NO code here)
    ├── PROGRESS_LOG.md            # Dated entries of what was built/fixed
    ├── FEATURE_STATUS.md          # Table: feature | status | notes
    ├── KNOWN_BUGS.md              # Bug tracker
    ├── ARCHITECTURE_NOTES.md      # Why decisions were made
    └── SESSION_SUMMARY.md         # Quick "where we left off" for each session
```

---

## 🎮 Game Concept

**Title (Working):** *Deus Ex Machina* — "God from the Machine"
*(or keep it open — you name it later)*

You are a **silent god** watching over a procedurally generated world. You don't play as a character — you **shape existence** from above. Civilizations rise, wars erupt, disasters cascade, and life evolves — all while you either watch or intervene using divine powers. The goal is **emergent storytelling** driven by simulation.

### How It Differs From WorldBox
| Feature | WorldBox | Our Game |
|---|---|---|
| Civilizations | Basic kingdoms | Full tech tree, diplomacy, culture |
| Disasters | Fire, rain, tornado | + Plagues, famines, volcanoes, eclipses |
| Ecology | Basic animals | Full food chain, migration, extinction |
| Magic | God spells only | Entities can learn/use magic naturally |
| World Events | Rare, scripted | Dynamic, triggered by simulation state |
| Entity depth | HP bar only | Hunger, age, mood, relationships, memory |
| God Powers | Click tools | Power tree (unlock by watching world evolve) |
| Seasons | No | 4 seasons affecting ecology + civilization |
| Underground | No | Cave layer with dungeons, ores, underworld entities |

---

## 🌐 World & Terrain

### World Size
- Default: **512 × 512 tiles** (chunked: 16×16 tiles per chunk)
- Chunk-based loading — only active/visible chunks are updated
- Zoom range: 1× (world overview) → 8× (tile detail)

### Tile Types
| Category | Tiles |
|---|---|
| Land | Grass, Dirt, Mud, Sand, Gravel, Snow, Ice, Obsidian, Ash |
| Water | Shallow Water, Deep Water, Swamp, Frozen Water |
| Terrain | Mountain, Hill, Cliff, Cave Entrance |
| Special | Sacred Ground, Corrupted Land, Lava, Void |

### Biomes
- Temperate Forest, Desert, Arctic Tundra, Tropical Jungle
- Swamp, Volcanic Region, Coastal, Grassland Plains
- Each biome determines: tile types, plant life, animal spawns, resource density, weather frequency

### World Generation Pipeline
```
Step 1: Elevation Map       ← Simplex Noise (2 octaves)
Step 2: Moisture Map        ← Simplex Noise (different seed)
Step 3: Temperature Map     ← Latitude + elevation modifier
Step 4: Biome Assignment    ← Whittaker diagram logic
Step 5: River Carving       ← Flow from high → low elevation
Step 6: Feature Placement   ← Trees, rocks, ores, ruins
Step 7: Entity Spawning     ← Based on biome
```

---

## 👥 Entities & AI

### Entity Categories
1. **Humans** — Settler, Farmer, Warrior, Archer, Priest, Merchant, Mage, King/Queen
2. **Animals** — Passive (deer, rabbit, cow, fish) | Predator (wolf, bear, hawk)
3. **Monsters** — Goblin, Orc, Skeleton, Vampire, Dragon, Demon, Lich
4. **Specials** — Ancient Guardians, Elemental beings, Wanderers

### Entity Stats
Every entity has:
- `HP`, `Attack`, `Defense`, `Speed`
- `Hunger`, `Age`, `Mood` (morale)
- `Faction`, `Relations[]` (likes/dislikes specific entities)
- `Memory[]` — remembers last N events (burned down, attacked, gifted food)
- `Traits[]` — Brave, Cowardly, Greedy, Faithful, Curious (affects AI behavior)

### AI Behavior (State Machine)
```
States: IDLE → WANDER → GATHER → BUILD → ATTACK → FLEE → DIE
Each state has priority scoring — highest score = active state
Traits modify score weights (Brave = lower FLEE priority)
```

---

## 🏰 Civilization System

### Progression Stages
```
Nomadic Tribe → Settlement → Village → Town → City → Kingdom → Empire
```

Each stage unlocks new buildings, population cap, and military capabilities.

### Tech Tree (Simplified)
```
Tier 1: Fire, Hunting, Shelter
Tier 2: Farming, Crafting, Writing
Tier 3: Iron Smelting, Walls, Religion
Tier 4: Siege Weapons, Alchemy, Trade Routes
Tier 5: Magic Research, Gunpowder, Naval
```

### Buildings
| Type | Purpose |
|---|---|
| Hut / House | Shelter, population |
| Farm / Mill | Food production |
| Barracks | Train warriors |
| Blacksmith | Craft weapons |
| Market | Enable trade |
| Temple | Raise morale, enable priests |
| Castle / Tower | Defense |
| Mage Tower | Enable magic research |
| Port | Naval + trade expansion |

### Diplomacy States
- Peace, Alliance, Rivalry, War, Tributary, Trade Agreement

---

## ⚡ God Powers (Player Toolkit)

### Power Tree (Unlocked by world progress)
```
CREATION BRANCH
  ├─ Spawn Creature (any entity)
  ├─ Place Tile
  ├─ Grow Forest
  └─ Raise/Lower Land

NATURE BRANCH
  ├─ Summon Rain
  ├─ Call Lightning
  ├─ Start Wildfire
  ├─ Freeze Region
  └─ Create River

DISASTER BRANCH
  ├─ Earthquake
  ├─ Meteor Strike
  ├─ Volcanic Eruption
  ├─ Plague (spread disease)
  └─ Flood

DIVINE BRANCH
  ├─ Bless (boost all stats of a civilization)
  ├─ Curse (weaken a civilization)
  ├─ Revelation (give tech advancement instantly)
  ├─ Smite (instant kill + area damage)
  └─ Resurrection (revive entity)

CHAOS BRANCH (late unlock)
  ├─ Corrupt Land (spreads, kills plants/animals)
  ├─ Summon Demon Army
  ├─ Dimensional Rift (portal spawning enemies)
  └─ World Tear (destroy chunk permanently)
```

### Power Cost System
- Each power costs **Divine Energy** (DE)
- DE regenerates passively over time
- More destructive = higher DE cost
- Bless/Curse civilizations who worship you → earn DE faster

---

## 🌦️ Weather & Seasons

### Seasons (each lasts in-game weeks)
| Season | Effect |
|---|---|
| Spring | Crops grow fast, animals breed |
| Summer | Max food production, drought risk |
| Autumn | Harvest bonus, migration begins |
| Winter | Crop failure, hunger, blizzard risk |

### Weather Events
- Light Rain, Heavy Rain, Thunderstorm
- Blizzard, Heatwave, Fog
- Acid Rain (post-volcanic), Blood Rain (chaos event)

---

## 💥 Disasters & Events

### Natural
- Earthquake — crack tiles, destroy buildings, trigger landslides
- Flood — water tiles expand, drown low-elevation areas
- Volcano — eruption damages surrounding tiles, spawns lava flow
- Wildfire — spreads across dry tiles, burns buildings/forests
- Meteor — mass destruction on impact, crater remains

### Biological
- Plague — spreads entity to entity, kills slowly, can wipe civilizations
- Famine — crop failure cascades into population drop
- Monster Invasion — scripted raid events on civilizations

### Civilization
- War (internal: civil war | external: kingdom war)
- Revolution (if king morale is terrible)
- Religious Schism (faction splits)

---

## 🎨 Graphics & Visual Plan

### Art Style
**16×16 pixel tiles** (upscaled 2× or 3× for display)
Palette: Earthy tones for terrain, vivid accents for effects and UI
Reference: RPG Maker-style + Stardew Valley terrain feel

### Tile Graphics Needed
- All biome tiles (at minimum 2 variants per tile for variety)
- Animated tiles: Water shimmer (4 frames), Lava flow (4 frames), Fire (6 frames)
- Transition tiles: Grass-to-sand edge, water shorelines, snow borders

### Entity Spritesheets
Each entity: **4-direction walk (4 frames each)** + idle + attack + death
- Human variants: skin tones, armor levels (naked → full plate)
- Animals: unique per species
- Monsters: distinctive silhouettes (no two should look alike)

### Building Sprites
- Each building has: **construction frame** → **complete frame** → **damaged frame** → **ruins frame**
- Larger buildings (castle, city hall): 2×2 or 3×3 tile sprites

### Effects (Visual Priority List)
| Effect | Technique | Priority |
|---|---|---|
| Fire | Particle system + animated sprite | HIGH |
| Rain | Line particles, angled streaks | HIGH |
| Snow | Dot particles, slow drift | HIGH |
| Explosion | Frame animation + particle burst | HIGH |
| Blood splash | Small red particles on hit | MEDIUM |
| God power beam | Glow surface + alpha pulse | HIGH |
| Plague cloud | Green particle cloud spreading | MEDIUM |
| Day/Night | Full-screen dark overlay + alpha tween | HIGH |
| Fog of War (optional) | Dark overlay per unexplored chunk | LOW |
| Ambient (leaves, dust) | Slow drifting particles | LOW |
| Water ripple | Circle expand + fade | MEDIUM |
| Lava glow | Yellow/orange tile tint pulses | MEDIUM |
| Lightning | White line flash + screen flash | MEDIUM |

### Lighting System (Pygame-only approach)
```python
# Create a dark surface overlay, cut circles for light sources
dark_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
dark_surface.fill((0, 0, 20, 160))   # Night color + alpha
# For each light source (fire, torch, magic):
pygame.draw.circle(dark_surface, (0,0,0,0), light_pos, light_radius)
screen.blit(dark_surface, (0,0))
```

### UI Art Style
- Dark stone texture panels (semi-transparent)
- Pixel font (e.g., Press Start 2P or Kenney's fonts)
- Gold/amber accent color for god powers
- Red health bars, green mood bars
- Icon-based toolbar (no text labels — hover shows tooltip)

---

## 🗺️ Minimap
- 120×120 pixel surface rendered in corner
- Each pixel = 1 tile, color-coded by biome
- Entity dots: white (humans), red (monsters), green (animals)
- Viewport rectangle shown as white outline
- Click minimap to pan camera there

---

## 📅 Development Phases

### Phase 0 — Foundation (Week 1–2)
- [ ] Pygame window, game loop, FPS cap
- [ ] Camera system (pan + zoom)
- [ ] Tilemap renderer (chunk-based)
- [ ] Simplex noise world generation
- [ ] Basic biome assignment
- [ ] Tile placement system

### Phase 1 — Life Begins (Week 3–4)
- [ ] Entity base class + entity manager
- [ ] Human entity with wander AI
- [ ] Animal entity (passive + predator)
- [ ] Basic rendering of entities with direction sprites
- [ ] Hunger + age + death cycle

### Phase 2 — Civilization (Week 5–7)
- [ ] Tribe → Village progression
- [ ] Building placement by AI
- [ ] Farming system
- [ ] Combat system (warriors attack enemies)
- [ ] Faction assignment + basic war

### Phase 3 — God Powers (Week 8–9)
- [ ] Power toolbar UI
- [ ] Spawn entity power
- [ ] Fire power (starts wildfire)
- [ ] Rain / lightning / meteor
- [ ] Divine energy system

### Phase 4 — Weather & Disasters (Week 10–11)
- [ ] Day/night cycle with lighting overlay
- [ ] Season system
- [ ] Rain/snow particle effects
- [ ] Earthquake + flood disasters
- [ ] Plague spreading system

### Phase 5 — Polish & Effects (Week 12–14)
- [ ] Particle system full implementation
- [ ] Animated tiles (water, fire, lava)
- [ ] Minimap
- [ ] Tooltip and entity info panel
- [ ] Sound effects (optional pygame.mixer)
- [ ] Main menu screen

### Phase 6 — Expansion (Week 15+)
- [ ] Underground cave layer
- [ ] Magic system for entities
- [ ] Full tech tree
- [ ] Trade routes between civilizations
- [ ] Mod-friendly data files (JSON configs for entities/biomes)

---

## 📝 Readme Folder — Log Format

### `PROGRESS_LOG.md` Entry Template
```markdown
## [DATE] — Session Title
**Duration:** ~X hours
**What was done:**
- Built chunk rendering system
- Fixed camera boundary bug

**Decisions made:**
- Chunk size set to 16×16 for performance

**Next session goal:**
- Start entity spawn system
```

### `FEATURE_STATUS.md` Table Format
```markdown
| Feature | Status | Notes |
|---|---|---|
| Tilemap rendering | ✅ Done | 16x16 chunks |
| World generation | ✅ Done | Simplex noise |
| Entity system | 🔄 In Progress | Base class done |
| Combat | ⏳ Planned | Phase 2 |
| God powers | ⏳ Planned | Phase 3 |
```

### `KNOWN_BUGS.md` Format
```markdown
## BUG-001 — [Short Title]
**Discovered:** [Date]
**Severity:** Low / Medium / High
**Description:** What happens
**Steps to reproduce:** ...
**Status:** Open / Fixed (fixed in commit/session on [date])
```

---

## ⚙️ Technical Notes (Pygame Specific)

### Performance Strategy
- **Chunk dirty flag** — only re-render chunks that changed
- **Entity active radius** — only run AI for entities within 3 chunks of camera
- **Surface caching** — pre-render static tile layers to surfaces
- **Particle pooling** — reuse particle objects instead of creating new ones

### Key Settings (`settings.py`)
```python
SCREEN_W, SCREEN_H = 1280, 720
TILE_SIZE = 16           # base pixel size
CHUNK_SIZE = 16          # tiles per chunk
FPS = 60
WORLD_W = 512            # tiles
WORLD_H = 512            # tiles
ZOOM_MIN = 1.0
ZOOM_MAX = 8.0
DAY_LENGTH = 3600        # frames per full day
SEASON_DAYS = 30         # in-game days per season
```

### Recommended Libraries
```
pygame          → core engine
noise           → Simplex/Perlin noise (pip install noise)
pytmx           → optional tilemap loader
json            → entity/biome config files
```

---

*Plan Version: 1.0 | Author: Erwin | Engine: Pygame (Python)*
