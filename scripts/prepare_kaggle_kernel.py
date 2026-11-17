#!/usr/bin/env python3
"""Prepare the exact Kaggle kernel slug confirmed by the Kaggle push URL."""
import argparse, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KAGGLE_DIR = ROOT / "kaggle" / "wan-run"
NOTEBOOK = KAGGLE_DIR / "wan_video.ipynb"
METADATA = KAGGLE_DIR / "kernel-metadata.json"
KERNEL_SLUG = "studio-almasawa-wan-video-generation"
KERNEL_TITLE = "Studio Almasawa Wan Video Generation"

parser = argparse.ArgumentParser()
parser.add_argument("--username", required=True)
parser.add_argument("--prompt", required=True)
parser.add_argument("--aspect-ratio", choices=("9:16", "16:9"), default="9:16")
args = parser.parse_args()

username = args.username.strip()
if not re.fullmatch(r"[A-Za-z0-9_-]+", username):
    raise SystemExit("KAGGLE_USERNAME contains unsupported characters.")
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
        source = re.sub(r'PROMPT = .*', "PROMPT = " + json.dumps(args.prompt, ensure_ascii=False), source, count=1)
        source = re.sub(r"WIDTH = \d+", f"WIDTH = {width}", source, count=1)
        source = re.sub(r"HEIGHT = \d+", f"HEIGHT = {height}", source, count=1)
        cell["source"] = source.splitlines(keepends=True)
        found = True
        break
if not found:
    raise SystemExit("Notebook prompt configuration cell was not found.")

NOTEBOOK.write_text(json.dumps(notebook, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
metadata = {
    "id": f"{username}/{KERNEL_SLUG}",
    "title": KERNEL_TITLE,
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
print(f"Prepared Kaggle kernel {username}/{KERNEL_SLUG}; aspect={args.aspect_ratio}; prompt_chars={len(args.prompt)}")
