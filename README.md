# Agent Sprite Forge Clean Align

Fork of [0x0funky/agent-sprite-forge](https://github.com/0x0funky/agent-sprite-forge) that keeps only the cleanup/alignment-focused skill:

- `skills/generate2dsprite-clean-align`

This fork intentionally does **not** include the upstream `generate2dsprite` or `generate2dmap` skills, so it is harder to confuse this variant with the original project.

## What This Skill Adds

`generate2dsprite-clean-align` is for generated sprite sheets that need quality-control postprocessing:

- preserve original generated resolution instead of downsampling to tiny preview cells
- remove magenta/pink background fringes with color-distance cleanup
- compare direct split, bbox center/feet alignment, and alpha-mask similarity alignment
- export transparent PNG sprite sheets and animated WebP previews
- generate side-by-side comparison HTML for visual QA

## Install

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo Sunwood-ai-labs/agent-sprite-forge-clean-align \
  --path skills/generate2dsprite-clean-align
```

Restart Codex after installing so the new skill name is picked up.

## Usage

Use the skill as:

```text
$generate2dsprite-clean-align
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
