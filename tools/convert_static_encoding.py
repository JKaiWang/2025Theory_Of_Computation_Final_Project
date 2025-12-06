#!/usr/bin/env python3
"""Convert files under web/static from CP950/Big5 (Windows ANSI) to UTF-8.

Usage:
    python tools/convert_static_encoding.py

This script makes a backup copy of files to web/static_backup before converting.
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = ROOT / "web" / "static"
BACKUP_DIR = ROOT / "web" / "static_backup"

EXTS = {".html", ".js", ".css"}


def ensure_backup():
    if not BACKUP_DIR.exists():
        print(f"Creating backup directory: {BACKUP_DIR}")
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        for p in STATIC_DIR.rglob("*"):
            rel = p.relative_to(STATIC_DIR)
            dst = BACKUP_DIR / rel
            if p.is_dir():
                dst.mkdir(parents=True, exist_ok=True)
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                with p.open("rb") as rf, dst.open("wb") as wf:
                    wf.write(rf.read())
    else:
        print(f"Backup already exists at {BACKUP_DIR}")


def convert_file(p: Path):
    try:
        # Read bytes and decode as cp950 (Big5) then write UTF-8
        b = p.read_bytes()
        try:
            text = b.decode("cp950")
        except Exception:
            # fallback: try utf-8 (if already utf-8)
            text = b.decode("utf-8")

        p.write_text(text, encoding="utf-8")
        print(f"Converted: {p}")
    except Exception as e:
        print(f"Failed to convert {p}: {e}")


def main():
    if not STATIC_DIR.exists():
        print("web/static not found; aborting.")
        return

    ensure_backup()

    for p in STATIC_DIR.rglob("*"):
        if p.suffix.lower() in EXTS and p.is_file():
            convert_file(p)

    print("Conversion complete. Please restart your server and clear browser cache (Ctrl+F5).")


if __name__ == "__main__":
    main()
