#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["fonttools"]
# ///
"""
Fixes two problems in NerdFont-patched Codevka fonts:
1. isFixedPitch = 0 -> macOS Font Book does not recognize the font as mo2. PostScript name (nameID=6) -> kitty +list-fonts --psnames does not show the fontnospace

Usage:
uv run fix-mono-font.py <fontfile>

Test if font is listed as monospace with `ghostty +list-fonts` or `kitty +list-fonts --psnames`
"""

import sys
from fontTools.ttLib import TTFont


def main():

    path = sys.argv[1]

    print(f"\n=== {path} ===")
    font = TTFont(path)

    # https://github.com/kiwi0fruit/open-fonts/blob/master/setisFixedPitch-fonttools.py
    # https://pypi.org/project/font-CLI/#ftcli-fix-monospace
    if font.has_key("post"):
        if font["post"].isFixedPitch == 0:
            font["post"].isFixedPitch = 1

    else:
        print("Post table not found")

    font.save(path)

    print(f"\nFont {path} fixed.")


if __name__ == "__main__":
    main()
