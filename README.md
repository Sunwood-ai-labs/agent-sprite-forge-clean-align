# Agent Sprite Forge Clean Align

Fork of [0x0funky/agent-sprite-forge](https://github.com/0x0funky/agent-sprite-forge) that keeps only the clean-align variants:

- `skills/generate2dsprite-clean-align`
- `skills/generate2dmap-clean-align`

This fork intentionally does **not** include the upstream `generate2dsprite` or `generate2dmap` skill folders under their original names, so it is harder to confuse this variant with the original project.

## What These Skills Add

`generate2dsprite-clean-align` is for generated sprite sheets that need quality-control postprocessing:

- preserve original generated resolution instead of downsampling to tiny preview cells
- remove magenta/pink background fringes with color-distance cleanup
- compare direct split, bbox center/feet alignment, and alpha-mask similarity alignment
- export transparent PNG sprite sheets and animated WebP previews
- generate side-by-side comparison HTML for visual QA

`generate2dmap-clean-align` is the matching map workflow fork:

- generate/edit production-oriented 2D maps, layered raster maps, tilemaps, prop packs, collision, and scene-hook metadata
- keep actor sprites and animation sheets out of map deliverables
- route reusable transparent props or actor assets to `$generate2dsprite-clean-align`
- preserve the upstream map pipeline while avoiding the upstream skill name

## Install

Install both fork skills:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo Sunwood-ai-labs/agent-sprite-forge-clean-align \
  --path skills/generate2dsprite-clean-align skills/generate2dmap-clean-align
```

Restart Codex after installing so the new skill name is picked up.

## Usage

Use the skills as:

```text
$generate2dsprite-clean-align
$generate2dmap-clean-align
```

The bundled comparison processor expects one folder per asset, each containing `raw-sheet.png`:

```bash
python3 skills/generate2dsprite-clean-align/scripts/process_3x3_alignment_variants.py \
  --raw-root ./raw-characters \
  --output-root ./clean-align-output \
  --duration 240
```

The output includes:

- `traditional/<asset>/`
- `bbox/<asset>/`
- `similarity/<asset>/`
- `index.html`

Each method folder includes transparent PNG frames, `sheet-transparent.png`, `animation-original.webp`, and `pipeline-meta.json`.
