# 🎨 Supplemental Module: Art & Color Palette Design Plan
*Plan Version: 1.1 | Added UI/UX Color Constraints*

---

## 1. Palette Philosophy: The "Vibrant Nature & Cosmic Magic" Palette

To match the **"silent god"** theme, the environment uses desaturated, earthy mid-tones so that player actions, magic, disasters, and UI elements pop with high-contrast, glowing vibrancy.

- **Color Restriction:** Stick to a **16-color or 32-color master palette** (like DB32 or Lospec50) to keep the 2D pixel art cohesive.
- **Shading Style:** Flat colors with selective outline shading. Avoid heavy dithering; let clean pixel clusters represent textures.

---

## 2. Hex Palette Allocations for Tiles & Biomes

### 🌊 Water & Depths

| Tile Type | Hex Code | Visual Purpose |
|---|---|---|
| Deep Water | `#1d2b53` | Midnight blue; deep ocean layers |
| Shallow Water | `#29adff` | Tropical cyan; coastlines and riverbeds |
| Swamp Water | `#1f3e3a` | Murky green-brown; low visibility |
| Ice / Frozen | `#abf6f0` | Pale glacial blue; reflective highlights |

### 🌿 Vegetation & Grasslands

| Tile Type | Hex Code | Visual Purpose |
|---|---|---|
| Temperate Grass | `#4ea746` | Vibrant mid-green; standard biome base |
| Jungle Moss | `#1b5220` | Deep, humid shadow green |
| Dry Grass / Plains | `#a3a04e` | Olive/khaki green; transition zones |
| Sacred Ground | `#7ee6ae` | Minty, radioactive-glowing green |

### 🏜️ Earth, Sand & Desolation

| Tile Type | Hex Code | Visual Purpose |
|---|---|---|
| Sand / Desert | `#f4ecc3` | Warm, soft cream; beaches and dunes |
| Dirt / Mud | `#5f4534` | Rich brown; plowed farms and riverbanks |
| Mountain / Rock | `#767a84` | Cool slate grey; high elevation |
| Ash / Volcanic | `#323339` | Near-black charcoal; dead regions |

---

## 3. FX, Entities & UI Lighting Color Palettes

### 🔥 Disasters & Magic (High Saturation)

- **Lava Flow / Fire:** Core `#ffec27` *(Bright Yellow)* → Outer `#ff004d` *(Crimson Red)*
- **Corrupted Land / Plague:** `#7a1c78` *(Plague Purple)* mixed with `#1b0e22` *(Void Black)*
- **Divine Powers:** `#fff1e8` *(Holy White)* bordered by `#ffcc00` *(Solar Gold)*

### 👥 Faction Accent Colors (For Entity Sprites & Banners)

To easily identify kingdoms on the map, use highly distinct 8-bit pure tones for armor trims, crowns, and banners:

| Kingdom | Hex Code | Identity |
|---|---|---|
| Kingdom A — Imperial | `#0041ca` | Royal Blue |
| Kingdom B — Tribal | `#b90000` | Blood Red |
| Kingdom C — Mage Order | `#ffd300` | Amber Gold |
| Kingdom D — Elven/Forest | `#00aa4f` | Emerald |

### 🖥️ UI Color Matrix

| UI Element | Hex Code | Notes |
|---|---|---|
| Background Panels | `#1a1c2c` | 90% alpha transparent dark navy stone |
| Borders / Accents | `#dfa650` | Burnished Gold |
| Health Bar | `#ff2424` | Health Red |
| Stamina / Mood Bar | `#24cc24` | Stamina/Mood Green |
| Mana / Divine Energy Bar | `#2488ff` | Mana/DE Blue |

---

## 4. Color Ramp Workflow for Pixel Artists

When drawing your **16×16 sprites**, use this **4-step color ramp rule** to ensure visual depth:

```
[ Shadow ]   ────►   [ Base ]     ────►   [ Highlight ] ────►   [ Godly Glow ]
 Low Light             True Color            Direct Sun             Magic Effect
 #3a2214               #5f4534               #a37252                #ffcc00
```

> **Rule of thumb:** Every sprite needs at minimum **Shadow + Base + Highlight**. The Godly Glow step is reserved for magic, divine, or corrupted variants only — don't use it on plain terrain.

---

## 5. Technical Implementation in Python (`settings.py`)

Store these hex values as standard **RGB tuples** inside your `settings.py` so your Pygame surface draws use the exact color design scheme:

```python
# settings.py - Color Palette Dictionary
PALETTE = {
    # --- Terrain Colors ---
    "DEEP_WATER":       (29,  43,  83),
    "SHALLOW_WATER":    (41,  173, 255),
    "SWAMP_WATER":      (31,  62,  58),
    "ICE":              (171, 246, 240),

    "GRASS":            (78,  167, 70),
    "JUNGLE_MOSS":      (27,  82,  32),
    "DRY_GRASS":        (163, 160, 78),
    "SACRED_GROUND":    (126, 230, 174),

    "SAND":             (244, 236, 195),
    "DIRT":             (95,  69,  52),
    "MOUNTAIN":         (118, 122, 132),
    "ASH":              (50,  51,  57),

    # --- FX & Hazards ---
    "LAVA_CORE":        (255, 236, 39),
    "FIRE_OUTER":       (255, 0,   77),
    "PLAGUE_PURPLE":    (122, 28,  120),
    "VOID_BLACK":       (27,  14,  34),
    "DIVINE_WHITE":     (255, 241, 232),
    "SOLAR_GOLD":       (255, 204, 0),

    # --- Faction Colors ---
    "FACTION_IMPERIAL": (0,   65,  202),
    "FACTION_TRIBAL":   (185, 0,   0),
    "FACTION_MAGE":     (255, 211, 0),
    "FACTION_ELVEN":    (0,   170, 79),

    # --- UI Elements ---
    "UI_BG":            (26,  28,  44,  230),   # Includes Alpha channel
    "UI_GOLD":          (223, 166, 80),
    "BAR_HEALTH":       (255, 36,  36),
    "BAR_MOOD":         (36,  204, 36),
    "BAR_DE":           (36,  136, 255),
}
```

### Usage Example in Pygame

```python
import pygame
from settings import PALETTE

# Drawing a tile
pygame.draw.rect(surface, PALETTE["GRASS"], tile_rect)

# Drawing a health bar
pygame.draw.rect(surface, PALETTE["BAR_HEALTH"], health_bar_rect)

# Drawing UI panel (with alpha)
panel_surface = pygame.Surface((width, height), pygame.SRCALPHA)
panel_surface.fill(PALETTE["UI_BG"])
screen.blit(panel_surface, panel_pos)
```

---

## 6. Quick Palette Reference Card

```
TERRAIN ─────────────────────────────────────────────────────
  Deep Water   #1d2b53 ██   Shallow Water  #29adff ██
  Swamp        #1f3e3a ██   Ice            #abf6f0 ██
  Grass        #4ea746 ██   Jungle         #1b5220 ██
  Dry Grass    #a3a04e ██   Sacred         #7ee6ae ██
  Sand         #f4ecc3 ██   Dirt           #5f4534 ██
  Mountain     #767a84 ██   Ash            #323339 ██

FX / MAGIC ──────────────────────────────────────────────────
  Lava Core    #ffec27 ██   Fire Outer     #ff004d ██
  Plague       #7a1c78 ██   Void           #1b0e22 ██
  Divine White #fff1e8 ██   Solar Gold     #ffcc00 ██

FACTIONS ────────────────────────────────────────────────────
  Imperial     #0041ca ██   Tribal         #b90000 ██
  Mage Order   #ffd300 ██   Elven          #00aa4f ██

UI ──────────────────────────────────────────────────────────
  Panel BG     #1a1c2c ██   Gold Border    #dfa650 ██
  Health       #ff2424 ██   Mood           #24cc24 ██
  Divine Energy#2488ff ██
```

---

*Supplemental to: `GAME_DESIGN_PLAN.md` | Save this in: `Readme/ART_COLOR_PALETTE_PLAN.md`*
