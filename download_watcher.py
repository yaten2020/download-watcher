## ###!/usr/bin/env python3
import os, time, shutil, logging, sys
from pathlib import Path

# --- Settings you can edit ---
DOWNLOADS = Path.home() / "Downloads"
LOG_FILE = Path.home() / "Library" / "Logs" / "download_watcher.log"

# Map of rules: each key is a folder name (relative to your home unless absolute),
# value is a list of file globs OR extensions. Add/adjust as you like.
RULES = { "/Users/ykumar/Library/CloudStorage/Dropbox/syncTOP/mindmaps": ["mindmap*.json", "*.mmp"], }

# Files/Extensions to ignore while still downloading or system files
IGNORE_SUFFIXES = {".download", ".crdownload", ".part", ".DS_Store"}

# How long a file size must remain unchanged before moving (sec)
STABLE_SECONDS = 10

# --- End of settings ---

def is_ignored(p: Path) -> bool:
    if p.name.startswith("."):
        return True
    if any(p.name.endswith(suf) for suf in IGNORE_SUFFIXES):
        return True
    return False

def is_stable(p: Path, seconds: int) -> bool:
    try:
        size1 = p.stat().st_size
        time.sleep(seconds)
        size2 = p.stat().st_size
        return size1 == size2
    except FileNotFoundError:
        return False

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def move_file(file_path: Path) -> bool:
    # Try each rule in order; first match wins
    for dest_rel, patterns in RULES.items():
        for pattern in patterns:
            if file_path.match(pattern):
                dest_dir = Path.home() / dest_rel if not os.path.isabs(dest_rel) else Path(dest_rel)
                ensure_dir(dest_dir)
                target = dest_dir / file_path.name
                # If name exists, append a counter
                counter = 1
                stem, suffix = file_path.stem, file_path.suffix
                while target.exists():
                    target = dest_dir / f"{stem} ({counter}){suffix}"
                    counter += 1
                shutil.move(str(file_path), str(target))
                logging.info(f"Moved: {file_path} -> {target}")
                return True
    return False

def main():
    ensure_dir(LOG_FILE.parent)
    logging.basicConfig(filename=str(LOG_FILE), level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s")
    if not DOWNLOADS.exists():
        logging.error(f"Downloads folder not found: {DOWNLOADS}")
        sys.exit(1)

    moved_count = 0
    for p in DOWNLOADS.iterdir():
        if not p.is_file() or is_ignored(p):
            continue
        # Skip very new files; let them finish writing
        if not is_stable(p, STABLE_SECONDS):
            continue
        try:
            if move_file(p):
                moved_count += 1
        except Exception as e:
            logging.exception(f"Failed to move {p}: {e}")

    if moved_count:
        logging.info(f"Done. Moved {moved_count} file(s).")

if __name__ == "__main__":
    main()
