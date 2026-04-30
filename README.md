# Agent Sprite Forge

Traditional Chinese README: [README.zh-TW.md](./README.zh-TW.md)

![Agent Sprite Forge Banner](./src/banner.png)

> Turn natural-language prompts into game-ready 2D sprites and layered 2D maps with Codex.
>
> Plan with an agent. Render with built-in image generation. Export clean transparent sheets, GIFs, maps, props, and collision-ready scene data.

## Showcase

### Text To Sprite

<table>
  <tr>
    <td align="center" width="33%">
      <img src="./src/goku-kame.gif" alt="Goku Kamehameha" width="192" />
      <br />
      <strong>Goku with Kamehameha</strong>
      <br />
      <code>help me to use $generate2dsprite to create a goku is attacking with Kamehameha</code>
    </td>
    <td align="center" width="33%">
      <img src="./src/naruto-rasengan.gif" alt="Naruto Rasengan" width="192" />
      <br />
      <strong>Naruto using Rasengan</strong>
      <br />
      <code>使用 $generate2dsprite 幫我做一個鳴人使用螺旋丸的元素</code>
    </td>
  </tr>
</table>

### Spell Bundle / Cast, Projectile, Impact

<table>
  <tr>
    <td align="center" width="33%">
      <img src="./src/cast.gif" alt="Fire mage cast animation" width="176" />
      <br />
      <strong>Cast</strong>
    </td>
    <td align="center" width="33%">
      <img src="./src/projectile.gif" alt="Fire mage projectile animation" width="176" />
      <br />
      <strong>Projectile</strong>
    </td>
    <td align="center" width="33%">
      <img src="./src/impact.gif" alt="Fire mage impact animation" width="176" />
      <br />
      <strong>Impact</strong>
    </td>
  </tr>
</table>

Prompt:

```text
Use  $generate2dsprite to create a fire mage cast animation with projectile and impact.
```

### Game Sprite / Four-Direction Walk

<table>
  <tr>
    <td align="center" width="25%">
      <img src="./src/down.gif" alt="Samurai walking down" width="144" />
      <br />
      <strong>Down</strong>
    </td>
    <td align="center" width="25%">
      <img src="./src/left.gif" alt="Samurai walking left" width="144" />
      <br />
      <strong>Left</strong>
    </td>
    <td align="center" width="25%">
      <img src="./src/right.gif" alt="Samurai walking right" width="144" />
      <br />
      <strong>Right</strong>
    </td>
    <td align="center" width="25%">
      <img src="./src/up.gif" alt="Samurai walking up" width="144" />
      <br />
      <strong>Up</strong>
    </td>
  </tr>
</table>

Prompt:

```text
Use Generate 2D Sprite to create a top-down 4x4 player_sheet for a wandering young samurai with a red scarf and short katana.
Make a four-direction walk sprite sheet with 4 frames per direction.
Row order: down, left, right, up.
Same character, same outfit, same proportions, same pixel scale in every frame.
Solid #FF00FF background.
Each frame must fit fully inside its cell, with clear margin on all sides.
Retro JRPG pixel-art style.
```

### Reference To Sprite

<table>
  <tr>
    <td align="center" width="35%">
      <img src="./src/ref1.jpg" alt="Reference crocodile" width="180" />
      <br />
      <strong>Reference</strong>
    </td>
    <td align="center" width="65%">
      <img src="./src/croc_stone_play.gif" alt="Crocodile playing with a stone" width="220" />
      <br />
      <strong>Generated sprite animation</strong>
      <br />
      <code>幫我使用 $generate2dsprite 做一個這隻鱷魚玩手上石頭的元素</code>
    </td>
  </tr>
  <tr>
    <td align="center" width="35%">
      <img src="./src/ref2.jpg" alt="Reference male character" width="180" />
      <br />
      <strong>Reference</strong>
    </td>
    <td align="center" width="65%">
      <img src="./src/cz.gif" alt="Male character teaching animation" width="220" />
      <br />
      <strong>Generated sprite animation</strong>
      <br />
      <code>Use  $generate2dsprite to create this male character teaching.</code>
    </td>
  </tr>
</table>

### Codex-Built Playable Game Showcases

End-to-end playable game prototypes designed and built with Codex, with sprites and props produced through `$generate2dsprite` and map scenes planned through `$generate2dmap` when the game needs structured maps. Some are one-shot prompt demos; others are iterative Godot assemblies with generated assets wired into real engine scenes.

#### Neon Breach — Cyberpunk Side-Scroller

<p align="center">
  <img src="./src/neon-breach.png" alt="Neon Breach cyberpunk side-scroller" width="720" />
</p>

Prompt:

```text
use $generate2dsprite to create a 2D side-scrolling game similar to Mega Man. It should include attack mechanics, map elements, and all the essential features. I would like you to design it, and all the necessary assets should be created using this skill. It needs to be an actually playable game, with a cyberpunk story setting.
```

#### 晴嵐御魂錄 — Sengoku-Era Pokémon-like

<table>
  <tr>
    <td align="center" width="50%">
      <img src="./src/pokemonlike2.png" alt="Sengoku starter selection screen" width="360" />
      <br />
      <strong>Starter selection</strong>
    </td>
    <td align="center" width="50%">
      <img src="./src/pokemonlike.png" alt="Sengoku battle screen" width="360" />
      <br />
      <strong>Battle scene</strong>
    </td>
  </tr>
</table>

Prompt:

```text
Use $generate2dsprite to create a 2D game similar to Pokemon. You only need to build one scene for now. It must include a starter monster selection mechanic, a battle screen, and all basic gameplay functions. I would like you to design all the elements and the story, and you can also decide which game engine to use. Use this skill to create any assets you need. The story should be set in the Sengoku period. Can you try putting this together for me?
Please also pay attention to the size of the elements (the generated sprites need to be proportionally correct when placed into the game), and a game map must be generated as well. Basically, just help me make a game like this—I believe you won't have any problem doing this with that skill! Just one scene is enough, and there's no need for too many monster characters. Let's just start with a few, and we can slowly expand on it later!
```

#### Forest Pass Defense — Godot Tower Defense

A Godot 4 tower-defense prototype assembled with Codex + agent-sprite-forge. This showcase goes beyond standalone asset generation: the map, separated props, towers, enemy animation sheets, boss/flying enemies, HUD icons, waves, difficulty settings, build/upgrade/sell flow, projectiles, and targeting rules are wired into a real Godot scene.

<p align="center">
  <img src="./src/kingdomrush-forest-pass.png" alt="Forest Pass Defense Godot tower-defense map" width="760" />
  <br />
  <strong>Godot tower-defense map with route layout, tower placements, props, and base defense area</strong>
</p>

<table>
  <tr>
    <td align="center" width="40%">
      <img src="./src/kingdomrush-enemy-roster.png" alt="Forest Pass Defense enemy roster with flyer and boss" width="320" />
      <br />
      <strong>Enemy roster, including flyer and boss units</strong>
    </td>
    <td align="center" width="30%">
      <img src="./src/kingdomrush-tower-icons.png" alt="Forest Pass Defense generated tower icons" width="260" />
      <br />
      <strong>Tower lineup</strong>
    </td>
    <td align="center" width="30%">
      <img src="./src/kingdomrush-hud-icons.png" alt="Forest Pass Defense generated HUD icons" width="260" />
      <br />
      <strong>HUD and gameplay icons</strong>
    </td>
  </tr>
</table>

Godot prototype output includes:

- `scenes/ForestPass.tscn` with base map, separated props, enemy paths, tower slots, and HUD nodes.
- Six tower families with generated tower art and upgrade stages.
- Animated enemy sheets for ground units, flying units, and boss encounters.
- Wave, difficulty, tower catalog, collision, route, and tower-slot metadata.
- Runtime build, upgrade, sell, projectile, and targeting behavior connected in Godot.

Pipeline:

```text
image_gen map + separated props + tower sheets + enemy animation sheets + HUD icons + Godot gameplay wiring
```

### Layered RPG Map / Clean HD Reference Pipeline

`$generate2dmap` now models maps as a production pipeline instead of a single strategy label. It chooses a visual model, runtime object model, collision model, art direction, and export target. For layered raster maps it defaults to a clean hand-painted HD game-map style for readability, generates a ground-only base map, uses that visible base as a wrapper reference for a dressed planning pass, batches small props into a 3x3 prop pack, extracts transparent props, places them with y-sort metadata, and composes a flattened preview.

<table>
  <tr>
    <td align="center" width="33%">
      <img src="./src/cyber-canal-base.png" alt="Ground-only cyberpunk canal RPG base map" width="300" />
      <br />
      <strong>Ground-only base map</strong>
    </td>
    <td align="center" width="33%">
      <img src="./src/cyber-canal-dressed-reference.png" alt="Dressed cyberpunk canal reference map" width="300" />
      <br />
      <strong>Dressed reference pass</strong>
    </td>
    <td align="center" width="33%">
      <img src="./src/cyber-canal-prop-pack.png" alt="Generated 3x3 cyberpunk canal prop pack" width="300" />
      <br />
      <strong>3x3 generated prop pack</strong>
    </td>
  </tr>
</table>

<p align="center">
  <img src="./src/cyber-canal-layered-preview.png" alt="Layered cyberpunk canal RPG map preview" width="720" />
  <br />
  <strong>Flattened layered RPG map preview</strong>
</p>

Pipeline:

```text
layered_raster + y_sorted_props + precise_shapes + trigger_zones + raw_canvas
```

Reference-guided layered maps use this flow:

1. Pick the art direction: `clean_hd` by default for readable game maps, `pixel_inspired` for a softer pixel-adjacent look, or `retro_pixel` only when the user asks for classic pixel art.
2. Generate a ground-only base map.
3. Show the base map in the conversation context and generate a dressed reference from it.
4. Generate one-by-one props or a tightly margined prop pack from the dressed reference.
5. Run soft-matte chroma-key cleanup with despill before extracting props when magenta fringe appears.
6. Compose the final runtime preview from the original base plus extracted transparent props.

### Godot Editable TileMap Export

`$generate2dmap` can also produce an editable Godot map project instead of a single flattened image. In this showcase, the image-generated tileset and 3x3 prop sheet are wired into a Godot 4.5 scene with editable `TileMapLayer` nodes, separate prop sprites, encounter grass `Area2D` zones, collision `StaticBody2D` blockers, exit zones, metadata JSON, and a debug player/camera for immediate inspection.

Prompt:

```text
幫我使用 Generate 2D Map 生成一個2d rpg的遊戲地圖, 要有分開的Props, 包含遇怪獸的草叢, 連接Godot遊戲引擎，做完之後要可以開啟godot進行所有的元素調整
```

<p align="center">
  <img src="./src/godot-editor.png" alt="Generate2DMap Godot editor scene with editable TileMapLayer and nodes" width="860" />
  <br />
  <strong>Godot editor scene: editable layers, props, zones, collision, exits, and debug player</strong>
</p>

<table>
  <tr>
    <td align="center" width="50%">
      <img src="./src/godot-meadow-layered-preview.png" alt="Godot meadow layered RPG map preview" width="360" />
      <br />
      <strong>Layered map preview</strong>
    </td>
    <td align="center" width="50%">
      <img src="./src/godot-meadow-debug-preview.png" alt="Godot meadow debug preview with collision and zones" width="360" />
      <br />
      <strong>Collision and zone debug overlay</strong>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <img src="./src/godot-meadow-tileset.png" alt="Image-generated Godot meadow tileset atlas" width="360" />
      <br />
      <strong>Image-generated tileset atlas</strong>
    </td>
    <td align="center" width="50%">
      <img src="./src/godot-meadow-prop-pack.png" alt="Image-generated 3x3 meadow prop pack" width="360" />
      <br />
      <strong>3x3 generated prop pack</strong>
    </td>
  </tr>
</table>

Godot output includes:

- Editable `TileMapLayer` nodes for ground, water/bridge, decor, encounter grass, and obstacles.
- `YSorted_SeparateProps` with independent `Sprite2D` props.
- Encounter grass `Area2D` zones with encounter tables.
- Collision `StaticBody2D` blockers for boundaries, water, cliffs, and prop bases.
- Exit `Area2D` zones for route transitions.
- A `CharacterBody2D` debug player with camera for opening and testing the scene immediately.

Pipeline:

```text
image_gen tileset + prop_pack_3x3 + layered_tilemap + separate_props + trigger_zones + Godot_TileMap
```

Codex-first 2D game asset skills for game-ready 2D sprites, props, FX, and playable map scenes.

This repository currently ships two skills:

- [`skills/generate2dsprite`](./skills/generate2dsprite): generate and postprocess sprites, animation sheets, props, and FX.
- [`skills/generate2dmap`](./skills/generate2dmap): choose a 2D map pipeline, generate base maps or prop packs, extract transparent props, compose previews, and produce collision/zones metadata.

`$generate2dmap` uses `$generate2dsprite` when the chosen map pipeline needs reusable transparent props. Small environmental props can be batched into `2x2`, `3x3`, or `4x4` prop packs, then extracted into individual transparent props. Simple maps can stay as a single baked image.

When a visual reference is involved, both skills use the same wrapper rule: make the image visible in the conversation first. Attached images and freshly generated images are already visible; local files should be opened with `view_image` before asking built-in image generation to preserve identity, style, map layout, or sprite lineage.

Codex is the primary target because Codex already has built-in image generation. That lets one agent handle the full loop:

1. Plan the asset or map pipeline.
2. Generate the raw sprite sheet, prop, or map image.
3. Run deterministic local post-processing for chroma-key cleanup, frame extraction, alignment, QC, and transparent PNG/GIF export.
4. Assemble map scenes with collision, zones, prop placement, prop-pack manifests, and preview images when needed.

The current focus is 2D game assets and map scenes, not full game-pack automation.

## What It Can Generate

- Creatures
- Characters
- Players and NPCs
- Spell casts
- Projectiles
- Impacts and explosions
- FX sheets
- Small bundles such as `unit_bundle`, `spell_bundle`, and `combat_bundle`
- Reference-guided sprite variants, animation sheets, and evolution lines
- Godot tower-defense prototypes with maps, props, towers, enemies, waves, HUD, and build/upgrade/sell flow
- Single baked 2D maps
- Clean HD hand-painted layered maps
- Layered base maps with transparent props
- Dressed-reference guided layered maps
- 2D map prop packs such as `2x2`, `3x3`, and `4x4`
- Collision and zone metadata for playable maps
- Flattened map previews for QA and showcase
- Godot-ready editable maps with `TileMapLayer`, separate props, `Area2D` encounter grass, `StaticBody2D` collision, exit zones, and debug player scenes

## Why Codex First

This repo is intentionally Codex-first because Codex can generate images directly inside the same workflow.

That gives you a much cleaner pipeline:

- No separate image API wiring
- No external sprite backend
- No extra prompt-builder service
- One agent decides the asset plan
- One local processor handles deterministic cleanup and export

The script is not the creative brain. The agent decides:

- Asset type
- Action type
- Bundle shape
- Sheet layout
- Frame count
- Alignment strategy
- Whether detached effects should be kept or filtered

The Python script only performs deterministic pixel operations.

## Repository Layout

```text
agent-sprite-forge/
  README.md
  README.zh-TW.md
  requirements.txt
  src/
  skills/
    generate2dmap/
      SKILL.md
      agents/
        openai.yaml
      references/
        layered-map-contract.md
        map-strategies.md
        prop-pack-contract.md
      scripts/
        compose_layered_preview.py
        extract_prop_pack.py
    generate2dsprite/
      SKILL.md
      agents/
        openai.yaml
      references/
        modes.md
        prompt-rules.md
      scripts/
        generate2dsprite.py
```

## Install

### Option 1: Windows PowerShell

Clone the repo, install the local processor dependencies, then copy both skills into your Codex skills directory:

```powershell
git clone https://github.com/0x0funky/agent-sprite-forge.git
cd .\agent-sprite-forge
python -m pip install -r .\requirements.txt
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force `
  ".\skills\*" `
  "$env:USERPROFILE\.codex\skills\"
```

### Option 2: macOS / Linux

```bash
git clone https://github.com/0x0funky/agent-sprite-forge.git
cd ./agent-sprite-forge
python3 -m pip install -r ./requirements.txt
mkdir -p ~/.codex/skills
cp -R ./skills/* ~/.codex/skills/
```

Start a new Codex session after installation so the skill is loaded cleanly.

## Python Requirements

The local post-processor depends on:

- `Pillow`
- `numpy`

They are listed in [`requirements.txt`](./requirements.txt). Codex handles image generation itself, but these Python packages are still needed for:

- Magenta background removal
- Frame splitting
- Bounding-box extraction
- Alignment and rescaling
- Transparent GIF and PNG export

## Suggested Prompts

### Basic

```text
Use  $generate2dsprite to create a 3x3 idle for an ultimate earth titan.
```

```text
Use  $generate2dsprite to create a side-view lightning knight attack animation.
```

```text
Use  $generate2dsprite to create a late-Sengoku player_sheet for a wandering fire swordsman.
```

### Spell / FX

```text
Use  $generate2dsprite to create a wizard spell bundle with cast, projectile, and impact sprites.
```

```text
Use  $generate2dsprite to create a fireball projectile loop and a matching explosion impact.
```

```text
Use  $generate2dsprite to create a side-view summon entrance effect for a thunder wolf spirit.
```

### Character / Monster Examples

```text
Use  $generate2dsprite to create Omegamon attack and right-move animation assets.
```

```text
Use  $generate2dsprite to create a golden divine boar 2x2 idle animation.
```

```text
Use  $generate2dsprite to create a Naruto-style rasengan cast sheet in 2x3.
```

### Map Examples

```text
Use $generate2dmap to create a small fixed-screen pixel-art battle arena with simple collision.
```

```text
Use $generate2dmap to create a top-down RPG forest shrine map. Use a layered raster pipeline, a 3x3 prop pack for small environmental props, precise collision, encounter grass zones, a rest point, and actors that can walk in front of and behind tall props.
```

```text
Use $generate2dmap to revise this existing map into a layered raster map. Keep the background baked, but split the gate and lanterns into reusable transparent props with y-sort placement metadata.
```

## What You Get

For a typical sheet output:

- `raw-sheet.png`
- `raw-sheet-clean.png`
- `sheet-transparent.png`
- Frame PNGs
- `animation.gif`
- `prompt-used.txt`
- `pipeline-meta.json`

For player walk sheets, you also get direction strips and per-direction GIFs.

For a map output, the result depends on the chosen pipeline:

- Single baked map: a complete map image, optional prompt file, and optional collision metadata.
- Layered raster map: a base map, generated prop folders or prop-pack extraction manifest, prop placement metadata, collision/zones metadata, and a flattened layered preview.

## Notes

- Best results come from prompts that clearly specify view, action, and the desired motion style.
- Large creatures often work better as `3x3 idle`.
- Small spells and projectiles often work better as `1x4`, `2x2`, or `2x3`.
- For commercial projects, prefer original characters or IP that you control.

## Star History

<a href="https://www.star-history.com/?repos=0x0funky%2Fagent-sprite-forge&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=0x0funky/agent-sprite-forge&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=0x0funky/agent-sprite-forge&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=0x0funky/agent-sprite-forge&type=date&legend=top-left" />
 </picture>
</a>

## License

MIT. See [LICENSE](./LICENSE).
