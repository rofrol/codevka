#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["fonttools"]
# ///
"""
Fixes two problems in NerdFont-patched Codevka fonts:
1. isFixedPitch = 0 -> macOS Font Book does not recognize the font as monospace
2. PostScript name (nameID=6) -> kitty +list-fonts --psnames does not show the font

Usage:
    uv run fix-nerd-font.py CodevkaNerdFont-Extended.ttf CodevkaNerdFont-ExtendedSemiLight.ttf

Or without arguments (processes all Codevka*.ttf in the current directory):
    uv run fix-nerd-font.py
"""

import sys
import glob
from fontTools.ttLib import TTFont

# Expected PostScript names after NerdFont patching.
# Key = substring of the filename, value = target PS name.
PS_NAME_MAP = {
    "ExtendedSemiLight": "CodevkaNerdFont-ExtendedSemiLight",
    "Extended":          "CodevkaNerdFont-Extended",
}

def fix_font(path: str) -> None:
    print(f"\n=== {path} ===")
    font = TTFont(path)

    # --- 1. isFixedPitch ---
    before = font["post"].isFixedPitch
    font["post"].isFixedPitch = 1
    print(f"  post.isFixedPitch:    {before} -> 1")

    # --- 2. OS/2 PANOSE bProportion = 9 (monospace) ---
    before_panose = font["OS/2"].panose.bProportion
    font["OS/2"].panose.bProportion = 9
    print(f"  OS/2.panose.bProp:   {before_panose} -> 9")

    # --- 3. PostScript name (nameID = 6) ---
    target_ps = None
    for fragment, ps_name in PS_NAME_MAP.items():
        if fragment in path:
            target_ps = ps_name
            break

    name_table = font["name"]
    for record in name_table.names:
        if record.nameID == 6:
            before_ps = record.toUnicode()
            if target_ps:
                # Encode according to platform (platformID 1 = Mac, 3 = Windows)
                if record.platformID == 3:
                    record.string = target_ps.encode("utf-16-be")
                else:
                    record.string = target_ps.encode("latin-1")
                print(f"  PostScript name:     '{before_ps}' -> '{target_ps}'")
            else:
                print(f"  PostScript name:     '{before_ps}' (unchanged - unknown file)")

    font.save(path)
    print(f"  Saved: {path}")


def main():
    files = sys.argv[1:] if len(sys.argv) > 1 else sorted(glob.glob("Codevka*.ttf"))

    if not files:
        print("No files found. Pass paths as arguments or run the script")
        print("in the directory containing Codevka*.ttf files.")
        sys.exit(1)

    for path in files:
        try:
            fix_font(path)
        except Exception as e:
            print(f"  ERROR: {e}")

    print("\nDone. You can now install the fonts via Font Book.")


if __name__ == "__main__":
    main()
