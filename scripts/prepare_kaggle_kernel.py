#!/usr/bin/env python3
"""Prepare a Kaggle notebook run without storing credentials in the repository."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KAGGLE_DIR = ROOT / "kaggle" / "wan-run"
NOTEBOOK = KAGGLE_DIR / "wan_video.ipynb"
METADATA = KAGGLE_DIR / "kernel-metadata.json"

parser = argparse.ArgumentParser()
parser.add_argument("--username", required=True)
parser.add_argument("--prompt", required=True)
parser.add_argument("--aspect-ratio", choices=("9:16", "16:9"), default="9:16")
args = parser.parse_args()

if not args.prompt.strip():
    raise SystemExit("Prompt must not be empty.")

notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
width, height = (832, 480) if args.aspect_ratio == "16:9" else (480, 832)

found = False
for cell in notebook.get("cells", []):
    if cell.get("cell_type") != "code":
        continue
    source = "".join(cell.get("source", []))
    if "# PROMPT_CONFIG" in source:
        source = source.replace('PROMPT = "__PROMPT__"', "PROMPT = " + json.dumps(args.prompt, ensure_ascii=False))
        source = source.replace("WIDTH = 480", f"WIDTH = {width}")
        source = source.replace("HEIGHT = 832", f"HEIGHT = {height}")
        cell["source"] = source.splitlines(keepends=True)
        found = True
        break

if not found:
    raise SystemExit("Notebook prompt configuration cell was not found.")

NOTEBOOK.write_text(json.dumps(notebook, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
metadata = {
    "id": f"{args.username}/studio-almasawa-wan-run",
    "title": "Studio Almasawa Wan Run",
    "code_file": "wan_video.ipynb",
    "language": "python",
    "kernel_type": "notebook",
    "is_private": True,
    "enable_gpu": True,
    "enable_internet": True,
    "dataset_sources": [],
    "competition_sources": [],
    "kernel_sources": [],
    "model_sources": []
}
METADATA.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Prepared private Kaggle kernel for {args.username}; aspect={args.aspect_ratio}; prompt_chars={len(args.prompt)}")
