#!/usr/bin/env python3
"""
Amethyst File Masking Tool (Non-Destructive Alternative to File Deletion)

Usage:
    python3 mask_tool.py list [mod_name]
    python3 mask_tool.py mask "<mod_name>" "<relative/path/to/file.ext>"
    python3 mask_tool.py unmask "<mod_name>" "<relative/path/to/file.ext>"
    python3 mask_tool.py status
"""

import os
import sys
import shutil

PROFILE_DIR = os.path.dirname(os.path.abspath(__file__))
MODS_DIR = os.path.join(PROFILE_DIR, "mods")

def list_masked(filter_mod=None):
    found = 0
    print("=== CURRENTLY MASKED (HIDDEN) FILES IN AMETHYST ===")
    for m in sorted(os.listdir(MODS_DIR)):
        if filter_mod and filter_mod.lower() not in m.lower():
            continue
        masked_dir = os.path.join(MODS_DIR, m, "_masked")
        if os.path.isdir(masked_dir):
            files = []
            for root, dirs, fnames in os.walk(masked_dir):
                for f in fnames:
                    rel = os.path.relpath(os.path.join(root, f), masked_dir)
                    files.append(rel)
            if files:
                print(f"\nMod: [{m}] ({len(files)} masked files)")
                for f in sorted(files):
                    print(f"  [MASKED] {f}")
                    found += 1
    if found == 0:
        print("No files are currently masked under _masked/ subdirectories.")
    else:
        print(f"\nTotal masked files: {found}")

def mask_file(mod_name, file_rel_path):
    mod_path = os.path.join(MODS_DIR, mod_name)
    if not os.path.isdir(mod_path):
        print(f"Error: Mod directory not found: {mod_path}")
        return False
    src = os.path.join(mod_path, file_rel_path)
    if not os.path.isfile(src):
        print(f"Error: Target file not found in mod: {src}")
        return False
    dst = os.path.join(mod_path, "_masked", file_rel_path)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.move(src, dst)
    print(f"Successfully MASKED:\n  From: {src}\n  To:   {dst}")
    print("When Amethyst deploys, this file will be excluded from the live game assets.")
    return True

def unmask_file(mod_name, file_rel_path):
    mod_path = os.path.join(MODS_DIR, mod_name)
    if not os.path.isdir(mod_path):
        print(f"Error: Mod directory not found: {mod_path}")
        return False
    src = os.path.join(mod_path, "_masked", file_rel_path)
    if not os.path.isfile(src):
        print(f"Error: Masked file not found: {src}")
        return False
    dst = os.path.join(mod_path, file_rel_path)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.move(src, dst)
    print(f"Successfully UNMASKED (Restored):\n  From: {src}\n  To:   {dst}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1].lower()
    if cmd == "list":
        filter_mod = sys.argv[2] if len(sys.argv) > 2 else None
        list_masked(filter_mod)
    elif cmd == "mask":
        if len(sys.argv) < 4:
            print("Usage: python3 mask_tool.py mask \"<mod_name>\" \"<file_path>\"")
            sys.exit(1)
        mask_file(sys.argv[2], sys.argv[3])
    elif cmd == "unmask":
        if len(sys.argv) < 4:
            print("Usage: python3 mask_tool.py unmask \"<mod_name>\" \"<file_path>\"")
            sys.exit(1)
        unmask_file(sys.argv[2], sys.argv[3])
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)
