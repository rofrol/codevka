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

# https://github.com/ryanoasis/nerd-fonts/blob/1514941a80397d93361f4193346d9cbb9ed21c6e/bin/scripts/fpfix.py
# https://github.com/kiwi0fruit/open-fonts/blob/master/setisFixedPitch-fonttools.py
# https://pypi.org/project/font-CLI/#ftcli-fix-monospace
import sys
from fontTools import ttLib

if len(sys.argv) < 2:
    sys.stderr.write(
        "# [Nerd Fonts] [fpfix.py] ERROR: Please enter a path to the font file"
    )
    sys.exit(1)

try:
    tt = ttLib.TTFont(sys.argv[1])
    post = tt["post"].__dict__
    post["isFixedPitch"] = 1
    tt.save(sys.argv[1])
    print(
        "# [Nerd Fonts] [fpfix.py]: '"
        + sys.argv[1]
        + "' fixed pitch setting was changed to 1 in the post table"
    )
except Exception as e:
    sys.stderr.write(
        "# [Nerd Fonts] [fpfix.py] ERROR: Unable to update the font isFixedPitch setting. "
        + str(e)
    )
    sys.exit(1)
