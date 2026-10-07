#!/usr/bin/env python3
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_PATTERN = "[0-9][0-9].json"
OUT_DIR = ROOT / "renamed_sources"
MAP_PATH = ROOT / "source_rename_map.json"


def sanitize_filename(name: str) -> str:
    # Keep human-readable names, but strip invalid filesystem chars.
    text = str(name).strip()
    text = text.replace("/", "-")
    text = text.replace("\\", "-")
    text = text.replace(":", "-")
    text = text.replace("*", "-")
    text = text.replace("?", "-")
    text = text.replace('"', "-")
    text = text.replace("<", "-")
    text = text.replace(">", "-")
    text = text.replace("|", "-")
    text = text.replace("\x00", "")
    text = re.sub(r"\s+", "_", text)
    text = text.replace("（", "(").replace("）", ")")
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "untitled"


def safe_js_name(name: str) -> str:
    clean = sanitize_filename(name)
    return f"{clean}.json"


def read_book_source_name(path: Path):
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return path.stem

    if isinstance(payload, list) and payload:
        item = payload[0]
        if isinstance(item, dict):
            value = item.get("bookSourceName")
            if value:
                return value
    return path.stem


def main():
    ROOT.mkdir(exist_ok=True)
    OUT_DIR.mkdir(exist_ok=True)

    mapping = {}
    for src_path in sorted(ROOT.glob(SRC_PATTERN)):
        name = read_book_source_name(src_path)
        target_name = safe_js_name(name)
        target_path = OUT_DIR / target_name

        # Avoid collisions by appending a numeric suffix when needed.
        counter = 1
        while target_path.exists():
            candidate = target_path.with_name(f"{target_name[:-5]}_{counter}.json")
            if not candidate.exists():
                target_path = candidate
                break
            counter += 1

        shutil.copy2(src_path, target_path)
        mapping[src_path.name] = target_path.name

    MAP_PATH.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Created {len(mapping)} renamed files in {OUT_DIR.name}.")
    print(f"Rename mapping saved to {MAP_PATH.name}.")


if __name__ == "__main__":
    main()
