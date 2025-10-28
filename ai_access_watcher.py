#!/usr/bin/env python3
# AI-ACCESS Minimal Watcher (Baseline Benchmark)
# Core purpose: verify file deployment loop and log integrity.

import os, time, shutil
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).parent
PROJECT = "AI-ACCESS"
ROOT = BASE / "projects" / PROJECT
INCOMING = ROOT / "incoming"
PRODUCTION = ROOT / "production"
HISTORY = ROOT / "_history"
DEVLOG = BASE / "devlog.txt"

def utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S.%fZ")

def log(line):
    DEVLOG.parent.mkdir(parents=True, exist_ok=True)
    with DEVLOG.open("a", encoding="utf-8") as f:
        f.write(f"[{utc()}] {line}\n")

def ensure_structure():
    for d in [INCOMING, PRODUCTION, HISTORY]:
        d.mkdir(parents=True, exist_ok=True)

def deploy(src):
    dest = PRODUCTION / src.name.replace("update_", "")
    hist = HISTORY / f"{utc()}_{dest.name}"
    if dest.exists():
        shutil.move(dest, hist)
        log(f"Archived: {hist}")
    shutil.move(src, dest)
    log(f"Deployed: {dest}")

def main():
    ensure_structure()
    log("Watcher started.")
    print("AI-ACCESS Watcher active. Press Ctrl+C to stop.")
    try:
        while True:
            for p in INCOMING.glob("update_*"):
                deploy(p)
            time.sleep(2)
    except KeyboardInterrupt:
        log("Watcher stopped.")

if __name__ == "__main__":
    main()
