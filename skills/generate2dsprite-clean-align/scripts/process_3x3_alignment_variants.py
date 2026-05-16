#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image


@dataclass(frozen=True)
class Method:
    key: str
    label: str
    note: str


METHODS = [
    Method("traditional", "従来法: そのまま3x3分割", "セル内の生成位置ずれを補正しない版"),
    Method("bbox", "補正版: 中心X + 足元Y 揃え", "bboxから中心と足元を合わせた版"),
    Method("similarity", "類似度補正: 形状重なり最大化", "アルファ形状の類似度で位置を探索した版"),
]


def display_name(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.replace("-", "_").split("_") if part)


def discover_characters(raw_root: Path) -> list[tuple[str, str]]:
    characters = []
    for child in sorted(raw_root.iterdir()):
        if child.is_dir() and (child / "raw-sheet.png").exists():
            characters.append((child.name, display_name(child.name)))
    if not characters:
        raise FileNotFoundError(f"No character folders with raw-sheet.png found under {raw_root}")
    return characters


def clean_magenta(im: Image.Image) -> Image.Image:
    """Chroma-key magenta and remove anti-aliased magenta fringes."""
    arr = np.array(im.convert("RGBA")).astype(np.float32)
    rgb = arr[..., :3]
    alpha = arr[..., 3]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]

    dist = np.sqrt((r - 255) ** 2 + g**2 + (b - 255) ** 2)
    magenta_like = (r > 135) & (b > 135) & (g < 175) & (np.abs(r - b) < 95) & (dist < 210)
    hard = magenta_like & (dist < 105)
    soft = magenta_like & (dist >= 105) & (dist < 210)

    alpha[hard] = 0
    fade = np.clip((dist - 105) / 105, 0, 1)
    alpha[soft] *= fade[soft]

    arr[..., :3] = rgb
    arr[..., 3] = alpha
    keyed = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
    return cleanup_magenta_edges(keyed)


def cleanup_magenta_edges(im: Image.Image, passes: int = 4) -> Image.Image:
    arr = np.array(im.convert("RGBA")).astype(np.uint8)
    for _ in range(passes):
        r, g, b, alpha = [arr[..., i] for i in range(4)]
        magenta = (
            (alpha > 0)
            & (r > 125)
            & (b > 125)
            & (g < 185)
            & (np.abs(r.astype(np.int16) - b.astype(np.int16)) < 110)
        )
        transparent = alpha < 12
        near = np.zeros_like(transparent)
        near[:-1, :] |= transparent[1:, :]
        near[1:, :] |= transparent[:-1, :]
        near[:, :-1] |= transparent[:, 1:]
        near[:, 1:] |= transparent[:, :-1]
        near[:-1, :-1] |= transparent[1:, 1:]
        near[1:, 1:] |= transparent[:-1, :-1]
        near[:-1, 1:] |= transparent[1:, :-1]
        near[1:, :-1] |= transparent[:-1, 1:]
        arr[..., 3] = np.where(magenta & near, 0, arr[..., 3])

    arrf = arr.astype(np.float32)
    r, g, b, alpha = [arrf[..., i] for i in range(4)]
    edge = (alpha > 0) & (alpha < 220) & (r > g + 30) & (b > g + 30) & (np.abs(r - b) < 120)
    pull = np.maximum(g, np.minimum(r, b) - 70)
    arrf[..., 0] = np.where(edge, np.minimum(r, pull + 30), r)
    arrf[..., 2] = np.where(edge, np.minimum(b, pull + 30), b)
    return Image.fromarray(np.clip(arrf, 0, 255).astype(np.uint8), "RGBA")


def split_raw(raw: Image.Image) -> list[Image.Image]:
    clean = clean_magenta(raw)
    width, height = clean.size
    cell_w, cell_h = width // 3, height // 3
    frames: list[Image.Image] = []
    for row in range(3):
        for col in range(3):
            box = (col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h)
            frames.append(clean.crop(box))
    return frames


def shift_image(im: Image.Image, dx: int, dy: int) -> Image.Image:
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.alpha_composite(im, (dx, dy))
    return out


def align_bbox(frames: list[Image.Image]) -> tuple[list[Image.Image], list[dict]]:
    boxes = [frame.getchannel("A").getbbox() for frame in frames]
    width, height = frames[0].size
    target_cx = width // 2
    target_bottom = min(max(box[3] for box in boxes if box), height - 18)
    aligned: list[Image.Image] = []
    report: list[dict] = []
    for idx, (frame, box) in enumerate(zip(frames, boxes), 1):
        if not box:
            aligned.append(frame)
            report.append({"frame": idx, "dx": 0, "dy": 0, "aligned_bbox": None})
            continue
        cx = (box[0] + box[2]) // 2
        dx = target_cx - cx
        dy = target_bottom - box[3]
        out = shift_image(frame, dx, dy)
        aligned.append(out)
        report.append({"frame": idx, "dx": dx, "dy": dy, "aligned_bbox": out.getchannel("A").getbbox()})
    return aligned, report


def shifted_array(arr: np.ndarray, dx: int, dy: int) -> np.ndarray:
    height, width = arr.shape
    out = np.zeros_like(arr)
    sx0, sx1 = max(0, -dx), min(width, width - dx)
    sy0, sy1 = max(0, -dy), min(height, height - dy)
    tx0, tx1 = max(0, dx), min(width, width + dx)
    ty0, ty1 = max(0, dy), min(height, height + dy)
    if sx1 > sx0 and sy1 > sy0:
        out[ty0:ty1, tx0:tx1] = arr[sy0:sy1, sx0:sx1]
    return out


def best_shift(ref: np.ndarray, cur: np.ndarray, search: int = 72, step: int = 3) -> tuple[int, int, float]:
    refb = (ref > 16).astype(np.float32)
    curb = (cur > 16).astype(np.float32)
    ref_sum = refb.sum()
    cur_sum = curb.sum()
    best_dx, best_dy, best_score = 0, 0, -1e18
    for dy in range(-search, search + 1, step):
        for dx in range(-search, search + 1, step):
            shifted = shifted_array(curb, dx, dy)
            inter = (refb * shifted).sum()
            union = ref_sum + cur_sum - inter + 1e-6
            score = inter / union - 0.00003 * (abs(dx) + abs(dy))
            if score > best_score:
                best_dx, best_dy, best_score = dx, dy, float(score)
    for dy in range(best_dy - step, best_dy + step + 1):
        for dx in range(best_dx - step, best_dx + step + 1):
            shifted = shifted_array(curb, dx, dy)
            inter = (refb * shifted).sum()
            union = ref_sum + cur_sum - inter + 1e-6
            score = inter / union - 0.00003 * (abs(dx) + abs(dy))
            if score > best_score:
                best_dx, best_dy, best_score = dx, dy, float(score)
    return best_dx, best_dy, best_score


def align_similarity(frames: list[Image.Image]) -> tuple[list[Image.Image], list[dict]]:
    alphas = [np.array(frame.getchannel("A"), dtype=np.float32) for frame in frames]
    ref_idx = 4
    ref = alphas[ref_idx]
    aligned: list[Image.Image] = []
    report: list[dict] = []
    for idx, (frame, alpha) in enumerate(zip(frames, alphas), 1):
        if idx - 1 == ref_idx:
            dx = dy = 0
            score = 1.0
        else:
            dx, dy, score = best_shift(ref, alpha)
        out = shift_image(frame, dx, dy)
        aligned.append(out)
        report.append(
            {
                "frame": idx,
                "dx": dx,
                "dy": dy,
                "similarity_score": round(score, 5),
                "aligned_bbox": out.getchannel("A").getbbox(),
            }
        )
    return aligned, report


def make_sheet(frames: list[Image.Image]) -> Image.Image:
    width, height = frames[0].size
    sheet = Image.new("RGBA", (width * 3, height * 3), (0, 0, 0, 0))
    for idx, frame in enumerate(frames):
        sheet.alpha_composite(frame, ((idx % 3) * width, (idx // 3) * height))
    return cleanup_magenta_edges(sheet)


def write_outputs(out_dir: Path, raw: Image.Image, frames: list[Image.Image], report: list[dict], method: Method, duration: int) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    raw.save(out_dir / "raw-sheet.png")
    clean_magenta(raw).save(out_dir / "raw-sheet-clean.png")
    cleaned_frames = [cleanup_magenta_edges(frame) for frame in frames]
    for idx, frame in enumerate(cleaned_frames, 1):
        frame.save(out_dir / f"idle-{idx}.png")
    sheet = make_sheet(cleaned_frames)
    sheet.save(out_dir / "sheet-transparent.png")
    cleaned_frames[0].save(
        out_dir / "animation-original.webp",
        "WEBP",
        save_all=True,
        append_images=cleaned_frames[1:],
        duration=duration,
        loop=0,
        lossless=True,
        method=6,
    )

    centers = []
    bottoms = []
    for frame in cleaned_frames:
        box = frame.getchannel("A").getbbox()
        if box:
            centers.append((box[0] + box[2]) // 2)
            bottoms.append(box[3])
    meta = {
        "method": method.key,
        "label": method.label,
        "note": method.note,
        "raw_size": list(raw.size),
        "rows": 3,
        "cols": 3,
        "cell_size": list(cleaned_frames[0].size),
        "sheet_size": list(sheet.size),
        "frame_count": len(cleaned_frames),
        "duration_ms": duration,
        "background_cleanup": "color-distance soft key plus transparent-edge magenta fringe cleanup",
        "center_range": [min(centers), max(centers)] if centers else None,
        "bottom_range": [min(bottoms), max(bottoms)] if bottoms else None,
        "alignment_report": report,
        "outputs": [
            "raw-sheet.png",
            "raw-sheet-clean.png",
            "sheet-transparent.png",
            "idle-1.png..idle-9.png",
            "animation-original.webp",
        ],
    }
    (out_dir / "pipeline-meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")


def render_html(out_root: Path, characters: list[tuple[str, str]]) -> None:
    chars_json = json.dumps(characters, ensure_ascii=False)
    methods_json = json.dumps([method.__dict__ for method in METHODS], ensure_ascii=False)
    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Integrated Sprite Processing Comparison</title>
    <style>
      :root {{ color-scheme: dark; --bg:#17191d; --panel:#22262d; --line:#3a404a; --text:#f4f1ea; --muted:#b9c0cb; --accent:#8dd3ff; --warn:#ffcf70; --ok:#8ff0b3; }}
      * {{ box-sizing: border-box; }}
      body {{ margin:0; min-height:100vh; background:var(--bg); color:var(--text); font-family:Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
      main {{ width:min(1500px, calc(100vw - 32px)); margin:0 auto; padding:28px 0 40px; }}
      header {{ display:flex; justify-content:space-between; gap:24px; align-items:end; margin-bottom:22px; }}
      h1 {{ margin:0 0 6px; font-size:28px; line-height:1.1; letter-spacing:0; }}
      .meta, figcaption {{ color:var(--muted); font-size:13px; line-height:1.45; }}
      .characters {{ display:grid; gap:20px; }}
      article {{ border:1px solid var(--line); border-radius:8px; background:var(--panel); padding:16px; overflow-x:auto; }}
      h2 {{ margin:0 0 14px; font-size:19px; letter-spacing:0; }}
      .compare {{ display:grid; grid-template-columns:repeat(3, minmax(470px, 1fr)); gap:16px; min-width:1450px; }}
      .method {{ border:1px solid var(--line); border-radius:8px; background:#1c2026; padding:12px; }}
      h3 {{ margin:0 0 10px; font-size:15px; letter-spacing:0; }}
      .traditional h3 {{ color:var(--warn); }} .bbox h3 {{ color:var(--ok); }} .similarity h3 {{ color:var(--accent); }}
      figure {{ margin:0; }} figure + figure {{ margin-top:12px; }}
      .checker {{ min-height:280px; display:grid; place-items:center; border:1px solid var(--line); overflow:hidden; background:linear-gradient(45deg,#d8d8d8 25%,transparent 25%),linear-gradient(-45deg,#d8d8d8 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#d8d8d8 75%),linear-gradient(-45deg,transparent 75%,#d8d8d8 75%); background-color:#f3f3f3; background-position:0 0,0 12px,12px -12px,-12px 0; background-size:24px 24px; }}
      img {{ max-width:100%; image-rendering:auto; }}
      .anim {{ width:min(100%, 360px); height:auto; }} .sheet {{ width:min(100%, 520px); height:auto; }}
      a {{ color:var(--accent); text-decoration:none; }} a:hover {{ text-decoration:underline; }}
      @media (max-width: 900px) {{ header {{ display:block; }} }}
    </style>
  </head>
  <body>
    <main>
      <header>
        <div>
          <h1>Integrated Sprite Processing Comparison</h1>
          <div class="meta">Background cleanup is included in every method. Compare direct split, bbox alignment, and similarity alignment.</div>
        </div>
        <div class="meta">Original resolution / animated WebP / transparent PNG sheets</div>
      </header>
      <section class="characters" id="characters"></section>
    </main>
    <script>
      const characters = {chars_json};
      const methods = {methods_json};
      const host = document.querySelector("#characters");
      for (const [slug, name] of characters) {{
        const article = document.createElement("article");
        article.innerHTML = `<h2>${{name}}</h2><div class="compare"></div>`;
        const compare = article.querySelector(".compare");
        for (const method of methods) {{
          const root = `${{method.key}}/${{slug}}`;
          const block = document.createElement("section");
          block.className = `method ${{method.key}}`;
          block.innerHTML = `
            <h3>${{method.label}}</h3>
            <figure>
              <div class="checker"><img class="anim" src="${{root}}/animation-original.webp?v=integrated" alt="${{name}} ${{method.label}} animation" /></div>
              <figcaption>${{method.note}}<br /><a href="${{root}}/animation-original.webp?v=integrated">animation-original.webp</a></figcaption>
            </figure>
            <figure>
              <div class="checker"><img class="sheet" src="${{root}}/sheet-transparent.png?v=integrated" alt="${{name}} ${{method.label}} sheet" /></div>
              <figcaption><a href="${{root}}/sheet-transparent.png?v=integrated">sheet-transparent.png</a></figcaption>
            </figure>`;
          compare.appendChild(block);
        }}
        host.appendChild(article);
      }}
    </script>
  </body>
</html>
"""
    (out_root / "index.html").write_text(html, encoding="utf-8")


def process(raw_root: Path, out_root: Path, duration: int) -> None:
    out_root.mkdir(parents=True, exist_ok=True)
    characters = discover_characters(raw_root)
    for slug, _name in characters:
        raw_path = raw_root / slug / "raw-sheet.png"
        if not raw_path.exists():
            raise FileNotFoundError(f"Missing raw sheet: {raw_path}")
        raw = Image.open(raw_path).convert("RGBA")
        frames = split_raw(raw)
        method_frames: dict[str, tuple[list[Image.Image], list[dict]]] = {
            "traditional": (frames, [{"frame": idx, "dx": 0, "dy": 0} for idx in range(1, 10)]),
            "bbox": align_bbox(frames),
            "similarity": align_similarity(frames),
        }
        for method in METHODS:
            write_outputs(out_root / method.key / slug, raw, *method_frames[method.key], method, duration)
        print(f"processed {slug}")
    render_html(out_root, characters)


def main() -> None:
    parser = argparse.ArgumentParser(description="Process Agent Sprite Forge 3x3 sheets with cleanup and alignment methods.")
    parser.add_argument(
        "--raw-root",
        type=Path,
        required=True,
        help="Folder containing one subfolder per asset, each with raw-sheet.png.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        required=True,
        help="Destination folder for traditional, bbox, similarity, and index.html outputs.",
    )
    parser.add_argument("--duration", type=int, default=240)
    args = parser.parse_args()
    process(args.raw_root, args.output_root, args.duration)


if __name__ == "__main__":
    main()
